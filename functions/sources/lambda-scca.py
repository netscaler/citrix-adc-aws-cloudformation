from barbarika.helpers import logger, get_gateway_ip, cidr_to_netmask
from barbarika.aws import send_response, wait_for_reachability_status
from barbarika.citrixadc import CitrixADC


def lambda_handler(event, context):
    MAX_RETRIES = 40
    fail_reason = None
    logger.info("event: {}".format(str(event)))
    request_type = event["RequestType"]
    response_status = "FAIED"
    response_data = {}
    try:
        if request_type == "Create":
            new_externaladc_password = event["ResourceProperties"]["CustomExternalADCPassword"]
            new_internaladc_password = event["ResourceProperties"]["CustomInternalADCPassword"]
            externaladc_instance_id = event["ResourceProperties"]["ExternalADCInstanceID"]
            externaladc_nsip = event["ResourceProperties"]["ExternalADCNSIP"]
            externaladc_vip = event["ResourceProperties"]["ExternalADCVIP"]
            # externaladc_snip = event['ResourceProperties']['ExternalADCSNIP']

            externaladc_management_subnet_cidr = event["ResourceProperties"]["ExternalADCManagementSubnetCIDR"]
            externaladc_client_subnet_cidr = event["ResourceProperties"]["ExternalADCClientSubnetCIDR"]
            externaladc_server_subnet_cidr = event["ResourceProperties"]["ExternalADCServerSubnetCIDR"]

            internaladc_instance_id = event["ResourceProperties"]["InternalADCInstanceID"]
            internaladc_nsip = event["ResourceProperties"]["InternalADCNSIP"]
            internaladc_vip = event["ResourceProperties"]["InternalADCVIP"]
            # internaladc_snip = event['ResourceProperties']['InternalADCSNIP']

            internaladc_management_subnet_cidr = event["ResourceProperties"]["InternalADCManagementSubnetCIDR"]
            internaladc_client_subnet_cidr = event["ResourceProperties"]["InternalADCClientSubnetCIDR"]
            # internaladc_server_subnet_cidr = event['ResourceProperties']['InternalADCServerSubnetCIDR']

            ubuntu_jumpbox_management_ip = event["ResourceProperties"]["UbuntuJumpboxManagementIP"]
            windows_jumpbox_management_ip = event["ResourceProperties"]["WindowsJumpboxManagementIP"]

            # TODO: check if the force-password change need to be taken care for secondary node also?
            externaladc = CitrixADC(
                nsip=externaladc_nsip,
                nsuser="nsroot",
                default_password=externaladc_instance_id,
                new_password=new_externaladc_password,
            )
            internaladc = CitrixADC(
                nsip=internaladc_nsip,
                nsuser="nsroot",
                default_password=internaladc_instance_id,
                new_password=new_internaladc_password,
            )

            # Check if the reachability status is "passed" for both the instances
            # so that bootstrapping is completed
            wait_for_reachability_status(
                status="passed",
                max_retries=MAX_RETRIES,
                adc_ip=externaladc_nsip,
                adc_instanceid=externaladc_instance_id,
            )
            wait_for_reachability_status(
                status="passed",
                max_retries=MAX_RETRIES,
                adc_ip=internaladc_nsip,
                adc_instanceid=internaladc_instance_id,
            )

            ssh_lbvservername = "lb-SSH"
            ssh_servicename = "serv-SSH"
            rdp_lbvservername = "lb-RDP"
            rdp_servicename = "serv-RDP"

            # External ADC Configuration
            externaladc.add_route(
                network_ip="0.0.0.0", netmask="0.0.0.0", gateway_ip=get_gateway_ip(externaladc_client_subnet_cidr),
            )
            externaladc.remove_route(
                network_ip="0.0.0.0", netmask="0.0.0.0", gateway_ip=get_gateway_ip(externaladc_management_subnet_cidr),
            )
            externaladc.add_route(
                network_ip=cidr_to_netmask(internaladc_client_subnet_cidr)[0],
                netmask=cidr_to_netmask(internaladc_client_subnet_cidr)[1],
                gateway_ip=get_gateway_ip(externaladc_server_subnet_cidr),
            )

            # SSH to Ubuntu Jumpbox
            externaladc.add_lbvserver(name=ssh_lbvservername, servicetype="TCP", ipaddress=externaladc_vip, port=22)
            externaladc.add_service(servicename=ssh_servicename, serviceip=internaladc_vip, servicetype="TCP", port=22)
            externaladc.bind_lbvserver_service(lbvserver_name=ssh_lbvservername, servicename=ssh_servicename)

            # RDP to Windows Jumbbox
            externaladc.add_lbvserver(name=rdp_lbvservername, servicetype="TCP", ipaddress=externaladc_vip, port=3389)
            externaladc.add_service(
                servicename=rdp_servicename, serviceip=internaladc_vip, servicetype="TCP", port=3389
            )
            externaladc.bind_lbvserver_service(lbvserver_name=rdp_lbvservername, servicename=rdp_servicename)

            # Internal ADC Configuration
            internaladc.add_route(
                network_ip="0.0.0.0", netmask="0.0.0.0", gateway_ip=get_gateway_ip(internaladc_client_subnet_cidr),
            )
            internaladc.remove_route(
                network_ip="0.0.0.0", netmask="0.0.0.0", gateway_ip=get_gateway_ip(internaladc_management_subnet_cidr),
            )

            # SSH to Ubuntu Jumpbox
            internaladc.add_lbvserver(name=ssh_lbvservername, servicetype="TCP", ipaddress=internaladc_vip, port=22)
            internaladc.add_service(
                servicename=ssh_servicename, serviceip=ubuntu_jumpbox_management_ip, servicetype="TCP", port=22,
            )
            internaladc.bind_lbvserver_service(lbvserver_name=ssh_lbvservername, servicename=ssh_servicename)

            # SSH to Ubuntu Jumpbox
            internaladc.add_lbvserver(name=rdp_lbvservername, servicetype="TCP", ipaddress=internaladc_vip, port=3389)
            internaladc.add_service(
                servicename=rdp_servicename, serviceip=windows_jumpbox_management_ip, servicetype="TCP", port=3389,
            )
            internaladc.bind_lbvserver_service(lbvserver_name=rdp_lbvservername, servicename=rdp_servicename)

            externaladc.set_cli_prompt(promptstring="%u@ExternalADC-%s")
            internaladc.set_cli_prompt(promptstring="%u@InternalADC-%s")

            externaladc.save_config()
            internaladc.save_config()

            response_status = "SUCCESS"
        else:  # request_type == 'Delete' | 'Update'
            response_status = "SUCCESS"
    except Exception as e:
        fail_reason = str(e)
        logger.error(fail_reason)
        response_status = "FAILED"
    finally:
        send_response(event, context, response_status, response_data, fail_reason=fail_reason)
