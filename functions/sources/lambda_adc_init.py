import os
from barbarika.helpers import logger
from barbarika.aws import send_response
from barbarika.citrixadc import CitrixADC


current_aws_region = os.environ["AWS_DEFAULT_REGION"]


def lambda_handler(event, context):
    fail_reason = None
    logger.info("event: {}".format(str(event)))
    request_type = event["RequestType"]
    response_status = "FAILED"
    response_data = {}
    try:
        if request_type == "Create":
            new_adc_password = event["ResourceProperties"]["CustomADCPassword"]
            adc_instance_id = event["ResourceProperties"]["ADCInstanceID"]
            adc_nsip = event["ResourceProperties"]["ADCPrivateNSIP"]
            new_rpc_password = event["ResourceProperties"]["RPCNodePassword"]

            adc = CitrixADC(
                nsip=adc_nsip, nsuser="nsroot", default_password=adc_instance_id, new_password=new_adc_password
            )
            logger.debug(adc.get_nsip())
            adc.change_rpcnode_password(nodeip=adc_nsip, new_rpc_password=new_rpc_password, secure="YES")
            adc.set_nsip_gui(gui="SECUREONLY")

            response_status = "SUCCESS"
        else:  # request_type == 'Delete' | 'Update'
            response_status = "SUCCESS"
    except Exception as e:
        fail_reason = str(e)
        logger.error(fail_reason)
        response_status = "FAILED"
    finally:
        send_response(event, context, response_status, response_data, fail_reason=fail_reason)
