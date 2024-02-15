import os
from barbarika.helpers import logger, waitfor
from barbarika.aws import send_response, wait_for_reachability_status
from barbarika.citrixadc import CitrixADC


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
            instance_id = event["ResourceProperties"]["ADCInstanceID"]
            nsip = event["ResourceProperties"]["ADCPrivateNSIP"]

            adm_ip = event["ResourceProperties"]["ADMIP"]
            licensing_mode = event["ResourceProperties"]["LicensingMode"]
            bandwidth = event["ResourceProperties"]["Bandwidth"]
            pooled_edition = event["ResourceProperties"]["PooledEdition"]
            platform = event["ResourceProperties"]["Platform"]
            cpu_edition = event["ResourceProperties"]["VCPUEdition"]

            # Check if the reachability status is "passed" for the instance
            # so that bootstrapping is completed
            wait_for_reachability_status(
                status="passed", max_retries=MAX_RETRIES, adc_ip=nsip, adc_instanceid=instance_id
            )

            adc = CitrixADC(nsip=nsip, nsuser="nsroot", default_password=instance_id, new_password=new_adc_password)

            adc.add_licenseserver(adm_ip)

            adc.allocate_pooled_license(licensing_mode, bandwidth, pooled_edition, platform, cpu_edition)
            adc.save_config()
            adc.reboot(warm=True)
            waitfor(200, reason="Warm rebooting {} ".format(adc.nsip))
            # The above reboot triggers ha-failover. So the secondaryADC becomes new-primaryADC
            # TODO: find out how to differentiate standalone vs ha deployment; primary.is_primarynode():
            # if deploymode.strip().upper() == 'HA':
            #     adc.hafailover()
            #     waitfor(
            #         60, reason='ADC {} is assuming primary node role'.format(adc.nsip))
            #     if not adc.is_primarynode():
            #         raise Exception(
            #             'ADC {} is not primary even after `force ha failover`')

            # Validate license
            adc.validate_pooled_license(licensing_mode, bandwidth, pooled_edition, platform, cpu_edition)

            adc.save_config()
            response_status = "SUCCESS"
        else:  # request_type == 'Delete' | 'Update'
            response_status = "SUCCESS"
    except Exception as e:
        fail_reason = str(e)
        logger.error(fail_reason)
        response_status = "FAILED"
    finally:
        send_response(event, context, response_status, response_data, fail_reason=fail_reason)
