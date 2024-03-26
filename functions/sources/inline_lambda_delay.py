import time
import cfnresponse
def handler(event, context):
  lambda_status = cfnresponse.SUCCESS
  lambda_reason = None
  resp = {}
  try:
    if event["RequestType"] == "Create":
      print("Request = Create")
      time_to_sleep = int(event["ResourceProperties"]["Sleep"])
      print(f"Sleeping(waiting) for {time_to_sleep} seconds")
      time.sleep(time_to_sleep)
  except Exception as e:
    print(f"Exception: {e}")
    lambda_status = cfnresponse.FAILED
    lambda_reason = str(e)
  finally:
    cfnresponse.send(event, context, lambda_status, responseData=resp, reason=lambda_reason)
