import urllib.request, urllib.parse
import json, random, string, time
import cfnresponse
HEADERS = {}
print_json = lambda x: json.dumps(x)
def open_url(url, headers, data=None, method='GET'):
  if data: data = data.encode('utf-8')
  req = urllib.request.Request(url, data, headers, method)
  try:
    with urllib.request.urlopen(req) as f:
      return f.status, f.reason, json.loads(f.read())
  except Exception as e:
    return e.code, e.reason, json.loads(e.read())
def get_token(client_id, client_secret):
  url = 'https://api-us.cloud.com/cctrustoauth2/root/tokens/clients'
  params = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
  params = urllib.parse.urlencode(params)
  return open_url(url, {}, params, 'POST')
def get_all_agents(customer_id):
  print("INSIDE get_all_agents()")
  agent_url = f'https://adm.cloud.com/massvc/{customer_id}/nitro/v2/config/mps_agent'
  status, reason, body = open_url(agent_url, HEADERS)
  print(f"Status={status}; Reason={reason}; Body={print_json(body)}")
  return body['mps_agent']
def get_agent(ip, customer_id):
    print("INSIDE get_agent()")
    all_agents = get_all_agents(customer_id)
    for agent in all_agents:
      if agent['name'] == ip and agent['platform'] == 'AWS':
        if agent['state'].upper() == 'UP':
          return agent
        print("Agent is still down. Waiting for it to come up.")
    return None
def create_new_profile(profilename, username, password, customer_id):
  print("INSIDE create_new_profile()")
  data = { "ns_device_profile": { "name": profilename, "username": username, "password": password, "snmpsecurityname": "test-snmp", } }
  url = f'https://adm.cloud.com/massvc/{customer_id}/nitro/v2/config/ns_device_profile'
  status, reason, body = open_url(url, HEADERS, json.dumps(data), 'POST')
  print(f"Status={status}; Reason={reason}; Body={print_json(body)}")
  if status != 200: # 409 CONFLICT if profile already exists
    raise Exception(f"Status={status}; Reason={reason}; Body={print_json(body)}")
  print(f"{profilename} Profile created")
def add_managed_adc(adcip, agentip, adcpass, profilename, customer_id):
  print("INSIDE add_managed_adc()")
  # check for existing managed device
  url = f'https://adm.cloud.com/massvc/{customer_id}/nitro/v2/config/managed_device'
  status, reason, body = open_url(url, HEADERS)
  print(f"Status={status}; Reason={reason}; Body={print_json(body)}")
  for managed_device in body['managed_device']:
    if managed_device['ip_address'] == adcip:
      print(f"{adcip} already exists")
      return status, reason, body
  MAX_RETRIES, tries = 30, 0
  agent = get_agent(agentip, customer_id)
  while agent is None and tries < MAX_RETRIES:
    agent = get_agent(agentip, customer_id)
    tries += 1
    print(f"Agent not found OR is still DOWN. Retrying in 10 seconds. Tries={tries}")
    time.sleep(10)
  dc_id = agent['datacenter_id']
  create_new_profile(profilename, 'nsroot', adcpass, customer_id)
  agent_id = agent['id']
  data =    {
    "params": { "action": "add_device" },
    "managed_device": {
      "register_failed_device": "true",
      "ip_address": adcip,
      "profile_name": profilename,
      "datacenter_id": dc_id,
      "agent_id": agent_id,
    }
  }
  url = f'https://adm.cloud.com/massvc/{customer_id}/nitro/v2/config/managed_device'
  status, reason, body = open_url(url, HEADERS, json.dumps(data), 'POST')
  print(f"Status={status}; Reason={reason}; Body={print_json(body)}")
  return status, reason, body
def wait_for_registration(body, customer_id):
  print("INSIDE wait_for_registration()")
  actid = body['managed_device'][0]['act_id']
  url = f'https://adm.cloud.com/massvc/{customer_id}/nitro/v2/config/activity_status/{actid}'
  status, reason, body = open_url(url, HEADERS)
  print(f"Status={status}; Reason={reason}; Body={print_json(body)}")
  for activity_status in body["activity_status"]:
    if activity_status['is_last'] == 'true':
      if activity_status['status'] == 'Completed':
        return True
      else:
        raise Exception(f"Status={status}; Reason={reason}; Body={print_json(body)}")
  return False
def check_for_adc_connectivity(adcip, adcpass):
  print("@check_for_adc_connectivity")
  MAX_RETRIES, tries = 100, 1
  url = f"http://{adcip}/nitro/v1/config/login"
  header = {'Content-Type': 'application/json'}
  data = { 'login': { 'username': adcip, 'password': adcpass, } }
  while tries <= MAX_RETRIES:
    status, reason, body = open_url(url, header, json.dumps(data), 'POST')
    print(f"Try: {tries}/{MAX_RETRIES}: status={status}; reason={reason}; body={body}")
    if status == 201:
      break
    tries += 1
    time.sleep(5)
def handler(event, context):
  global HEADERS
  lambda_status = cfnresponse.SUCCESS
  lambda_reason = None
  resp = {}
  try:
    if event["RequestType"] == "Create":
      print("Request = Create")
      customer_id = event["ResourceProperties"]["CustomerID"]
      client_id = event["ResourceProperties"]["ClientID"]
      client_secret = event["ResourceProperties"]["ClientSecret"]
      adcip = event["ResourceProperties"]["ADCIP"]
      agentip = event["ResourceProperties"]["AgentIP"]
      adcpass = event["ResourceProperties"]["ADCPassword"]
      profilename = event["ResourceProperties"]["ProfileName"]
      print(f"agentip:{agentip}; adcip:{adcip}; profilename:{profilename}")
      check_for_adc_connectivity(adcip, adcpass)
      status, reason, body = get_token(client_id, client_secret)
      if status != 200:
        raise Exception(f"Status={status}; Reason={reason}; Body={print_json(body)}")
      HEADERS = { 'Authorization': f"CwsAuthbearer={body['access_token']}", 'isCloud': 'true'}
      profilename += ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
      status, reason, body = add_managed_adc(adcip, agentip,adcpass, profilename, customer_id)
      if status != 200:
        raise Exception(f"Status={status}; Reason={reason}; Body={print_json(body)}")
      MAX_TRIES, tries = 20, 1
      while tries <= MAX_TRIES:
        status = wait_for_registration(body, customer_id)
        if not status:
          tries += 1
          print(f"ADC not registered yet. Retrying in 5 seconds. Tries={tries}")
          time.sleep(5)
        else:
          print("ADC registered successfully. ")
          break
      else:
        raise Exception(f"Device not registered after {MAX_TRIES} tries")
  except Exception as e:
    print(f"Exception: {e}")
    lambda_status = cfnresponse.FAILED
    lambda_reason = str(e)
  finally:
    cfnresponse.send(event, context, lambda_status, responseData=resp, reason=lambda_reason)
