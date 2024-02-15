import os
from barbarika.helpers import logger
from barbarika.aws import send_response, get_latest_citrixadc_ami


def lambda_handler(event, context):
    current_aws_region = os.environ["AWS_DEFAULT_REGION"]
    fail_reason = None
    logger.info("event: {}".format(str(event)))
    request_type = event["RequestType"]
    response_status = "FAILED"
    response_data = {}
    try:
        if request_type == "Create":
            adc_version = event["ResourceProperties"]["ADCVersion"]
            adc_product = event["ResourceProperties"]["ADCProduct"]

            response_data["LatestADCAMI"] = get_latest_citrixadc_ami(adc_version, adc_product)
            logger.info(
                "Latest ADC AMI for Region:{}, ADCVersion:{} and ADCProduct:{}".format(
                    current_aws_region, adc_version, adc_product
                )
            )
            response_status = "SUCCESS"
        else:  # request_type == 'Delete' | 'Update'
            response_status = "SUCCESS"
    except Exception as e:
        fail_reason = str(e)
        logger.error(fail_reason)
        response_status = "FAILED"
    finally:
        send_response(event, context, response_status, response_data, fail_reason=fail_reason)


if __name__ == "__main__":
    adc_version = "13.1"
    adc_product = "Citrix ADC VPX - Customer Licensed"
    print(get_latest_citrixadc_ami(adc_version, adc_product))
