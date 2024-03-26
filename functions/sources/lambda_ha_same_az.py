import os
from barbarika.helpers import logger, waitfor
from barbarika.aws import (
    send_response,
    get_subnet_address,
    wait_for_reachability_status,
    assign_secondary_ip_address,
    get_vip_eni,
    get_snip_eni,
    get_vip_subnet,
    get_snip_subnet,
    allocate_eip,
    associate_eip,
)
from barbarika.citrixadc import CitrixADC


current_aws_region = os.environ["AWS_DEFAULT_REGION"]


def lambda_handler(event, context):
    MAX_RETRIES = 60
    fail_reason = None
    logger.info("event: {}".format(str(event)))
    request_type = event["RequestType"]
    response_status = "FAILED"
    response_data = {}
    client_eip = ""
    try:
        if request_type == "Create":
            new_adc_password = event["ResourceProperties"]["CustomADCPassword"]
            primary_instance_id = event["ResourceProperties"]["PrimaryADCInstanceID"]
            primary_nsip = event["ResourceProperties"]["PrimaryADCPrivateNSIP"]
            # primary_vip = event['ResourceProperties']['PrimaryADCPrivateVIP']
            # primary_snip = event['ResourceProperties']['PrimaryADCPrivateSNIP']
            assign_eip2client = event["ResourceProperties"]["ClientENIEIP"]

            # vip_subnet = event['ResourceProperties']['ClientSubnetID']
            # snip_subnet = event['ResourceProperties']['ServerSubnetID']

            secondary_instance_id = event["ResourceProperties"]["SecondaryADCInstanceID"]
            secondary_nsip = event["ResourceProperties"]["SecondaryADCPrivateNSIP"]
            # secondary_vip = event['ResourceProperties']['SecondaryADCPrivateVIP']
            new_rpc_password = event["ResourceProperties"]["RPCNodePassword"]

            new_primaryadc_password = new_secondaryadc_password = new_adc_password

            # Check if the reachability status is "passed" for both the instances
            # so that bootstrapping is completed
            wait_for_reachability_status(
                status="passed", max_retries=MAX_RETRIES, adc_ip=primary_nsip, adc_instanceid=primary_instance_id,
            )
            wait_for_reachability_status(
                status="passed", max_retries=MAX_RETRIES, adc_ip=secondary_nsip, adc_instanceid=secondary_instance_id,
            )

            primary = CitrixADC(
                nsip=primary_nsip,
                nsuser="nsroot",
                default_password=primary_instance_id,
                new_password=new_primaryadc_password,
            )
            secondary = CitrixADC(
                nsip=secondary_nsip,
                nsuser="nsroot",
                default_password=secondary_instance_id,
                new_password=new_secondaryadc_password,
            )
            # assign VIP, SNIP to primaryADC
            primary_vip_eni = get_vip_eni(instid=primary_instance_id)
            primary_snip_eni = get_snip_eni(instid=primary_instance_id)

            # Only one floating secondary VIP and SNIP are assigned for now
            floating_vip = assign_secondary_ip_address(primary_vip_eni)[0]
            floating_snip = assign_secondary_ip_address(primary_snip_eni)[0]

            # If `ClientENIEIP` is Yes, assign EIP to this floating_vip
            if assign_eip2client == "Yes":
                client_eip, allocation_id = allocate_eip()
                associate_eip(allocation_id, primary_vip_eni, floating_vip)

            vip_subnet = get_vip_subnet(instid=primary_instance_id)
            snip_subnet = get_snip_subnet(instid=primary_instance_id)

            vip_subnetmask = get_subnet_address(vip_subnet)[1]
            snip_subnetmask = get_subnet_address(snip_subnet)[1]

            primary.add_nsip(ip=floating_vip, netmask=vip_subnetmask, iptype="VIP")
            primary.add_nsip(ip=floating_snip, netmask=snip_subnetmask, iptype="SNIP")

            primary.add_hanode(id=1, ipaddress=secondary_nsip, incmode=False)
            waitfor(10)
            secondary.add_hanode(id=1, ipaddress=primary_nsip, incmode=False)

            # Wait for the password to sync into Secondary-VPX.
            waitfor(60, reason="secondary VPX password to get synced to that of primary")

            primary.change_rpcnode_password(nodeip=primary_nsip, new_rpc_password=new_rpc_password)
            primary.change_rpcnode_password(nodeip=secondary_nsip, new_rpc_password=new_rpc_password)

            # From now, the Secondary-VPX password will be that of Primary-VPX
            secondary.change_password(new_primaryadc_password)

            primary.set_nsip_gui(gui="SECUREONLY")
            secondary.set_nsip_gui(gui="SECUREONLY")

            # ipset_name = 'qs_ipset'
            lbvserver_name = "qs_lbvserver"

            primary.add_lbvserver(name=lbvserver_name, servicetype="HTTP", ipaddress=floating_vip, port=80)

            waitfor(20, reason="for the HA Sync to complete")
            if secondary.get_lbvserver(name=lbvserver_name):
                logger.info("SUCCESS: {} and {} configured in HA mode".format(primary.nsip, secondary.nsip))
            else:
                logger.error("FAIL: Could not configure {} and {} in HA mode".format(primary.nsip, secondary.nsip))

            # # From now, the Secondary-VPX password will be that of Primary-VPX
            # secondary = CitrixADC(
            #     nsip=secondary_nsip, nsuser="nsroot", nspass=primary_instance_id)

            # ipset_name = 'qs_ipset'
            # lbvserver_name = 'qs_lbvserver'

            # primary.add_ipset(name=ipset_name)
            # secondary.add_ipset(name=ipset_name)

            # subnetmask = get_subnet_address(primary_vip_subnet)[1]
            # primary.add_nsip(ip=secondary_vip,
            #                  netmask=subnetmask, iptype='VIP')

            # primary.bind_ipset(name=ipset_name, ipaddress=secondary_vip)
            # secondary.bind_ipset(name=ipset_name, ipaddress=secondary_vip)

            # primary.add_lbvserver(name=lbvserver_name, servicetype='HTTP',
            #                       ipaddress=primary_vip, port=80, ipset=ipset_name)

            # if secondary.get_lbvserver(name=lbvserver_name):
            #     logger.info('SUCCESS: {} and {} configured in HA mode'.format(
            #         primary.nsip, secondary.nsip))
            # else:
            #     logger.error('FAIL: Could not configure {} and {} in HA mode'.format(
            #         primary.nsip, secondary.nsip))

            primary.configure_features(["LB", "CS", "SSL", "WL", "CR", "GSLB"])

            primary.save_config()
            secondary.save_config()

            response_data["client_eip"] = client_eip
            response_data["floating_vip"] = floating_vip
            response_data["floating_snip"] = floating_snip

            response_status = "SUCCESS"
        else:  # request_type == 'Delete' | 'Update'
            response_status = "SUCCESS"
    except Exception as e:
        fail_reason = str(e)
        logger.error(fail_reason)
        response_status = "FAILED"
    finally:
        send_response(event, context, response_status, response_data, fail_reason=fail_reason)
