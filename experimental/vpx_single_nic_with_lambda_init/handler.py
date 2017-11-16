import logging
from botocore.vendored import requests
import boto3
import urllib2
import time
import json
import socket
import struct

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2_client = boto3.client('ec2')


def get_subnet_mask(az, vpc_id, subnet_ids):
    filters = [{'Name': 'availability-zone', 'Values': [az]},
               {'Name': 'vpc-id', 'Values': [vpc_id]}]
    subnets = ec2_client.describe_subnets(SubnetIds=subnet_ids, Filters=filters)
    for subnet in subnets['Subnets']:
        cidr_block = subnet['CidrBlock']
        subnet_len = int(cidr_block.split('/')[1])
        mask = (1 << 32) - (1 << 32 >> subnet_len)
        subnet_mask = socket.inet_ntoa(struct.pack('>L', mask))
        return subnet_mask
    return None


def get_instance(instance_id):
    ec2_reservations = ec2_client.describe_instances(InstanceIds=[instance_id])
    for reservation in ec2_reservations['Reservations']:
        ec2_instances = reservation['Instances']
        for ec2_instance in ec2_instances:
            if ec2_instance['State']['Name'] == 'running':
                return ec2_instance
    return None


def send_response(event, context, response_status, response_data, physical_resource_id=None):
    response_url = event['ResponseURL']

    logger.info('Lambda Backed Custom resource response: going to respond to ' + response_url)

    response_body = {}
    response_body['Status'] = response_status
    response_body['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    response_body['PhysicalResourceId'] = physical_resource_id or context.log_stream_name
    response_body['StackId'] = event['StackId']
    response_body['RequestId'] = event['RequestId']
    response_body['LogicalResourceId'] = event['LogicalResourceId']
    response_body['Data'] = response_data

    json_response_body = json.dumps(response_body)

    logger.info('Lambda Backed Custom resource Response body:\n' + json_response_body)

    headers = {
        'content-type': '',
        'content-length': str(len(json_response_body))
    }

    try:
        response = requests.put(response_url,
                                data=json_response_body,
                                headers=headers)
        logger.info('Lambda Backed Custom resource response success: Status code: ' + response.reason)
    except Exception as e:
        logger.info('Lambda Backed Custom resource response: Failed to post response to ' +
                    response_url + ': ' + str(e))


def save_config(instance_id, ns_url):
    url = ns_url + 'nitro/v1/config/nsconfig?action=save'

    jsons = '{"nsconfig":{}}'
    logger.info('Initiating NITRO call to save config')
    result = do_nitro_call_with_retry(instance_id, url, jsons, timeout=10, max_retries=3)
    if not result[0]:
        raise Exception('Failed to save config reason=' + result[1])


def configure_features(instance_id, ns_url, features):
    url = ns_url + 'nitro/v1/config/nsfeature?action=enable'

    feat = {'nsfeature': {'feature': features}}
    jsons = json.dumps(feat)
    logger.info('Initiating NITRO call to configure features')
    result = do_nitro_call_with_retry(instance_id, url, jsons, timeout=10, max_retries=3)
    if not result[0]:
        raise Exception('Failed to configure features reason=' + result[1])


def do_nitro_call_with_retry(instance_id, url, json_data, timeout, max_retries=9):
    ns_password = instance_id

    retry_count = 0
    retry = True
    success = False
    failure_reason = ''

    headers = {'Content-Type': 'application/json', 'X-NITRO-USER': 'nsroot', 'X-NITRO-PASS': ns_password}
    r = urllib2.Request(url, data=json_data, headers=headers)
    while retry:
        try:
            logger.info('Initiating NITRO call to ' + url + ', data=' + json_data)
            urllib2.urlopen(r, timeout=timeout)
            logger.info('NITRO call to ' + url + ', data=' + json_data + ' succeeded!')
            retry = False
            success = True
        except urllib2.HTTPError as hte:
            if hte.code != 409:
                logger.info('HTTP Error making NITRO call: Error code: ' +
                            str(hte.code) + ', reason=' + hte.reason)
                retry = False
                failure_reason = 'NITRO error ' + str(hte.code) + ', reason=' + hte.reason
                if hte.code == 503 or hte.code == 599 or hte.code == 401:
                    # service unavailable or internal error, just sleep and try again
                    logger.info('NS VPX is not ready to be configured, service unavailable condition, may retry...')
                    retry = True
                    retry_count += 1
                    if retry_count > max_retries:
                        logger.info('Too many retries, giving up, retries=' + str(retry_count))
                        retry = False
                        success = False
                        failure_reason = 'Too many retries due to NITRO error ' +\
                                         str(hte.code) + ', reason=' + hte.reason
                        break
                    logger.info('NS VPX is not ready to be configured, retrying in 10 seconds')
                    time.sleep(10)
            else:
                logger.info('409 conflict: NS VPX already configured, no-op')
                success = True
                retry = False
        except urllib2.URLError as ure:
            logger.info('URLError during NITRO call: reason=' + str(ure.reason))
            if type(ure.reason).__name__ == 'timeout':
                logger.info('Socket timeout configuring NS VPX')
                retry_count += 1
                if retry_count > 9:
                    logger.info('Too many timeouts: giving up on configuring NS VPX')
                    retry = False
                    failure_reason = 'Too many retries due to socket timeouts'
                    success = False
                    break
                logger.info('NS VPX is not ready to be configured, retrying in 10 seconds')
                time.sleep(10)
            else:
                logger.info('Error configuring NS VPX: Irrecoverable error')
                retry = False
                failure_reason = 'Irrecoverable URL error'
                success = False
    return (success, failure_reason)


def configure_ip(instance_id, ns_url, ip, subnet_mask, ip_type):
    url = ns_url + 'nitro/v1/config/nsip'
    logger.info('Configuring NSIP: ip= ' + ip + ', mask=' + subnet_mask + ', type=' + ip_type)

    jsons = '{{"nsip":{{"ipaddress":"{}", "netmask":"{}", "type":"{}"}}}}'.format(ip, subnet_mask, ip_type)
    result = do_nitro_call_with_retry(instance_id, url, jsons, timeout=10, max_retries=9)
    if not result[0]:
        raise Exception('Failed to configure NSIP, type=' + ip_type + ', reason=' + result[1])


def lambda_handler(event, context):
    logger.info(str(event))
    request_type = event['RequestType']
    result = 'SUCCESS'
    data = {}
    if request_type == 'Create':
        try:
            instance_id = event['ResourceProperties']['EC2InstanceId']
            nsip = event['ResourceProperties']['PublicNSIP']
            subnet_id = event['ResourceProperties']['SubnetId']

            instance = get_instance(instance_id)
            if instance is None:
                logger.warn("Bailing since we couldn't find the instance id")
                raise Exception('Bailing since we could not find the instance id')

            az = instance['Placement']['AvailabilityZone']
            vpc_id = instance['VpcId']
            vip = instance['NetworkInterfaces'][0]['PrivateIpAddresses'][1]['PrivateIpAddress']
            snip = instance['NetworkInterfaces'][0]['PrivateIpAddresses'][2]['PrivateIpAddress']
            subnet_mask = get_subnet_mask(az, vpc_id, [subnet_id])
            ns_url = 'http://{}:80/'.format(nsip)  # TODO:https
            logger.info('ns_url=' + ns_url)
            logger.info('Going to add a SNIP to the NSIP ENI')
            configure_ip(instance_id, ns_url, snip, subnet_mask, 'snip')
            logger.info('Going to add a VIP to the NSIP ENI')
            configure_ip(instance_id, ns_url, vip, subnet_mask, 'vip')
            logger.info('Going to configure features')
            configure_features(instance_id, ns_url, ['LB', 'CS', 'SSL', 'WL'])
            save_config(instance_id, ns_url)
            data['SNIP'] = snip
            data['VIP'] = vip
        except Exception as e:
            logger.info('Failed to create custom resource ' + event['LogicalResourceId'] + ' in ' +
                        event['StackId'] + ' in response to ' + event['RequestId'] + ': ' + str(e))
            result = 'FAILED'

        send_response(event, context, result, data)
    elif request_type == 'Delete':
        send_response(event, context, 'SUCCESS', {})
    elif request_type == 'Update':
        send_response(event, context, 'SUCCESS', {})
