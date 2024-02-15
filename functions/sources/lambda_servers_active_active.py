import os
from barbarika.helpers import logger
from barbarika.aws import send_response, get_subnet_address, get_subnet_gateway, wait_for_reachability_status
from barbarika import CitrixADC


current_aws_region = os.environ["AWS_DEFAULT_REGION"]


def lambda_handler(event, context):
    MAX_RETRIES = 60
    fail_reason = None
    logger.info("event: {}".format(str(event)))
    request_type = event["RequestType"]
    response_status = "FAILED"
    response_data = {}
    try:
        if request_type == "Create":
            new_adc_password = event["ResourceProperties"]["CustomADCPassword"]
            primary_instance_id = event["ResourceProperties"]["PrimaryADCInstanceID"]
            primary_nsip = event["ResourceProperties"]["PrimaryADCPrivateNSIP"]
            primary_server_subnet = event["ResourceProperties"]["PrimaryADCServerPrivateSubnetID"]

            secondary_instance_id = event["ResourceProperties"]["SecondaryADCInstanceID"]
            secondary_nsip = event["ResourceProperties"]["SecondaryADCPrivateNSIP"]
            secondary_server_subnet = event["ResourceProperties"]["SecondaryADCServerPrivateSubnetID"]

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

            # Primary ADC to send traffic to all the servers (even in other availability zone)
            primary_server_subnet_address = get_subnet_address(primary_server_subnet)
            secondary_server_subnet_address = get_subnet_address(secondary_server_subnet)
            primary_server_gateway = get_subnet_gateway(primary_server_subnet)
            secondary_server_gateway = get_subnet_gateway(secondary_server_subnet)
            primary.add_route(
                network_ip=secondary_server_subnet_address[0],
                netmask=secondary_server_subnet_address[1],
                gateway_ip=primary_server_gateway,
            )
            secondary.add_route(
                network_ip=primary_server_subnet_address[0],
                netmask=primary_server_subnet_address[1],
                gateway_ip=secondary_server_gateway,
            )

            primary.save_config()
            secondary.save_config()

            response_status = "SUCCESS"
        else:  # request_type == 'Delete' | 'Update'
            response_status = "SUCCESS"
    except Exception as e:
        fail_reason = str(e)
        logger.error(fail_reason)
        response_status = "FAILED"
    finally:
        send_response(event, context, response_status, response_data, fail_reason=fail_reason)
