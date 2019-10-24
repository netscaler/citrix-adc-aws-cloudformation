import sys
import traceback

if sys.version_info[0] != 3:
    raise Exception('Can only run under python3')

import json
import codecs
import socket
import http.client
import urllib.request
import urllib.error
import urllib.parse
import ssl
import logging
import time
import argparse
from botocore.vendored import requests
import boto3
import struct


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())


ec2_client = boto3.client('ec2')


def get_subnet_mask(subnet_ids):
    filters = []
    subnets = ec2_client.describe_subnets(
        SubnetIds=subnet_ids, Filters=filters)
    logger.info('subnets: {}'.format(subnets))
    for subnet in subnets['Subnets']:
        cidr_block = subnet['CidrBlock']
        subnet_len = int(cidr_block.split('/')[1])
        mask = (1 << 32) - (1 << 32 >> subnet_len)
        subnet_mask = socket.inet_ntoa(struct.pack('>L', mask))
        logger.info('subnet_mask: {}'.format(subnet_mask))
        return subnet_mask
    return None


def waitfor(seconds, reason=None):
    if reason != None:
        logger.info(
            'Waiting for {} seconds. Reason: {}'.format(seconds, reason))
    else:
        logger.info('Waiting for {} seconds'.format(seconds))
    time.sleep(seconds)


def open_url(url, headers, data=None, method=None):
    method = 'GET' if method is None else method

    logger.debug("{}: {}".format(method, url))
    logger.debug("HEADERS: {}".format(json.dumps(headers, indent=4)))
    if data:
        logger.debug("DATA: {}".format(json.dumps(from_json(data), indent=4)))

    request = urllib.request.Request(
        url=url,
        headers=headers,
        data=data,
        method=method,
    )

    # Give a 3 seconds sleep for the command to get execute on
    waitfor(3)

    info = dict(url=url)
    r = None
    try:
        # We do not verify SSL
        context = ssl.SSLContext()
        context.verify_mode = ssl.CERT_NONE

        # Do the HTTP request
        r = urllib.request.urlopen(request, context=context)
        info.update(dict((k.lower(), v) for k, v in r.info().items()))
    except urllib.error.HTTPError as e:
        try:
            body = e.read()
        except AttributeError:
            body = ''

        # Try to add exception info to the output but don't fail if we can't
        try:
            # Lowercase keys, to conform to py2 behavior, so that py3 and py2 are predictable
            info.update(dict((k.lower(), v) for k, v in e.info().items()))
        except Exception:
            pass

        info.update({'msg': str(e), 'body': body, 'status': e.code})
    except urllib.error.URLError as e:
        code = int(getattr(e, 'code', -1))
        info.update(dict(msg="Request failed: %s" % str(e), status=code))
    except socket.error as e:
        info.update(dict(msg="Connection failure: %s" % str(e), status=-1))
    except http.client.BadStatusLine as e:
        info.update(dict(msg="Connection failure: connection was closed before a valid response was received: %s" % str(
            e.line), status=-1))
    except Exception as e:
        info.update(dict(msg="An unknown error occurred: %s" % str(e), status=-1),
                    exception=traceback.format_exc())

    return r, info


def to_json(data):
    return codecs.encode(json.dumps(data))


def from_json(data):
    return json.loads(data)


class NitroAPIOpener(object):

    def __init__(self, nsip, nitro_protocol='http', api_path='nitro/v1/config', nitro_user=None, nitro_pass=None, nitro_auth_token=None, mas_proxy_call=False, instance_ip=None, instance_name=None, instance_id=None):

        self.nitro_protocol = nitro_protocol
        self.nsip = nsip
        self.instance_id = instance_id

        self.r = None
        self.info = None
        self.api_path = api_path

        # Prepare the http headers according to module arguments
        self._headers = {}
        self._headers['Content-Type'] = 'application/json'

        # Check for conflicting authentication methods
        have_token = nitro_auth_token is not None
        have_userpass = None not in (nitro_user, nitro_pass)

        # if have_token and have_userpass:
        #     self.fail_module(
        #         msg='Cannot define both authentication token and username/password')

        if have_token:
            self._headers['Cookie'] = "NITRO_AUTH_TOKEN=%s" % nitro_auth_token

        if have_userpass:
            self._headers['X-NITRO-USER'] = nitro_user
            self._headers['X-NITRO-PASS'] = nitro_pass

        # Do header manipulation when doing a MAS proxy call
        if mas_proxy_call:
            if instance_ip is not None:
                self._headers['_MPS_API_PROXY_MANAGED_INSTANCE_IP'] = instance_ip
            elif instance_name is not None:
                self._headers['_MPS_API_PROXY_MANAGED_INSTANCE_NAME'] = instance_name
            elif instance_id is not None:
                self._headers['_MPS_API_PROXY_MANAGED_INSTANCE_ID'] = instance_id
            else:
                raise Exception(
                    'Target netscaler is undefined for MAS proxied NITRO call')

    def edit_response_data(self, r, info, result):
        '''
            Parses the r and info values from ansible fetch
            and manipulates the result accordingly
        '''

        # Save raw values to corresponding member variables
        self.r = r
        self.info = info

        # Search for body in both http body and http data
        if r is not None:
            result['http_response_body'] = codecs.decode(r.read(), 'utf-8')
        elif 'body' in info:
            result['http_response_body'] = codecs.decode(info['body'], 'utf-8')
            del info['body']
        else:
            result['http_response_body'] = ''

        result['http_response_data'] = info
        try:
            result['http_response_code'] = r.getcode()
        except AttributeError:
            result['http_response_code'] = 0

        # Update the nitro_* parameters

        # Nitro return code in http data
        result['nitro_errorcode'] = None
        result['nitro_message'] = None
        result['nitro_severity'] = None

        if result['http_response_body'] != '':
            try:
                data = from_json(result['http_response_body'])

                # Get rid of the string representation if json parsing succeeds
                del result['http_response_body']
            except ValueError:
                data = {}
            result['data'] = data
            result['nitro_errorcode'] = data.get('errorcode')
            result['nitro_message'] = data.get('message')
            result['nitro_severity'] = data.get('severity')

    def _construct_query_string(self, args=None, attrs=None, filter=None, action=None, count=False):

        query_dict = {}

        args = {} if args is None else args
        attrs = [] if attrs is None else attrs
        filter = {} if filter is None else filter

        # Construct args
        args_val = ','.join(
            ['%s:%s' % (k, urllib.parse.quote(args[k], safe='')) for k in args])

        if args_val != '':
            args_val = 'args=%s' % args_val

        # Construct attrs
        attrs_val = ','.join(attrs)
        if attrs_val != '':
            attrs_val = 'attrs=%s' % attrs_val

        # Construct filters
        filter_val = ','.join(['%s:%s' % (k, filter[k]) for k in filter])
        if filter_val != '':
            filter_val = 'filter=%s' % filter_val

        # Construct action
        action_val = ''
        if action is not None:
            action_val = 'action=%s' % action

        # Construct count
        count_val = ''
        if count:
            count_val = 'count=yes'

        # Construct the query string
        # Filter out empty string parameters
        val_list = [args_val, attrs_val, filter_val, action_val, count_val]
        query_params = '&'.join([v for v in val_list if v != ''])

        if query_params != '':
            query_params = '?%s' % query_params

        return query_params

    def put(self, put_data, resource, id=None):

        if id != None:
            url = '%s://%s/%s/%s/%s' % (
                self.nitro_protocol,
                self.nsip,
                self.api_path,
                resource,
                id,
            )
        else:
            url = '%s://%s/%s/%s' % (
                self.nitro_protocol,
                self.nsip,
                self.api_path,
                resource
            )

        data = to_json(put_data)

        r, info = open_url(
            url=url,
            headers=self._headers,
            data=data,
            method='PUT',
        )

        result = {}
        self.edit_response_data(r, info, result)

        return result

    def get(self, resource, id=None, args=None, attrs=None, filter=None):

        args = {} if args is None else args
        attrs = [] if attrs is None else attrs
        filter = {} if filter is None else filter

        # Construct basic get url
        url = '%s://%s/%s/%s' % (
            self.nitro_protocol,
            self.nsip,
            self.api_path,
            resource,
        )

        # Append resource id
        if id is not None:
            url = '%s/%s' % (url, id)

        query_params = self._construct_query_string(
            args=args, attrs=attrs, filter=filter)

        # Append query params
        url = '%s%s' % (url, query_params)

        r, info = open_url(
            url=url,
            headers=self._headers,
            method='GET',
        )

        result = {}
        self.edit_response_data(r, info, result)

        return result

    def delete(self, resource, id=None, args=None):

        args = {} if args is None else args

        # Deletion by name takes precedence over deletion by attributes

        url = '%s://%s/%s/%s' % (
            self.nitro_protocol,
            self.nsip,
            self.api_path,
            resource
        )

        # Append resource id
        if id is not None:
            url = '%s/%s' % (url, id)

        # Append query params
        query_params = self._construct_query_string(args=args)
        url = '%s%s' % (url, query_params)

        r, info = open_url(
            url=url,
            headers=self._headers,
            method='DELETE',
        )

        result = {}
        self.edit_response_data(r, info, result)

        return result

    def post(self, post_data, resource, action=None):

        # Construct basic get url
        url = '%s://%s/%s/%s' % (
            self.nitro_protocol,
            self.nsip,
            self.api_path,
            resource,
        )

        query_params = self._construct_query_string(action=action)

        # Append query params
        url = '%s%s' % (url, query_params)

        data = to_json(post_data)

        r, info = open_url(
            url=url,
            headers=self._headers,
            data=data,
            method='POST',
        )

        result = {}
        self.edit_response_data(r, info, result)

        return result

    def reachability_status(self):
        response = ec2_client.describe_instance_status(
            Filters=[],
            InstanceIds=[self.instance_id],
        )

        r_status = response['InstanceStatuses'][0]['InstanceStatus']['Details'][0]['Status']
        logger.debug('Rechability Status for {}: {}'.format(
            self.nsip, r_status))
        return r_status.strip()


def send_response(event, context, response_status, response_data, physical_resource_id=None):
    response_url = event['ResponseURL']

    logger.info(
        'Lambda Backed Custom resource response: going to respond to ' + response_url)

    response_body = {}
    response_body['Status'] = response_status
    response_body['Reason'] = 'See the details in CloudWatch Log Stream: ' + \
        context.log_stream_name
    response_body['PhysicalResourceId'] = physical_resource_id or context.log_stream_name
    response_body['StackId'] = event['StackId']
    response_body['RequestId'] = event['RequestId']
    response_body['LogicalResourceId'] = event['LogicalResourceId']
    response_body['Data'] = response_data

    json_response_body = json.dumps(response_body)

    logger.info('Lambda Backed Custom resource Response body:\n' +
                json_response_body)

    headers = {
        'content-type': '',
        'content-length': str(len(json_response_body))
    }

    try:
        response = requests.put(response_url,
                                data=json_response_body,
                                headers=headers)
        logger.info(
            'Lambda Backed Custom resource response success: Status code: ' + response.reason)
    except Exception as e:
        logger.info('Lambda Backed Custom resource response: Failed to post response to ' +
                    response_url + ': ' + str(e))


def configure_features(opener, featurelist):
    post_data = {'nsfeature': {'feature': featurelist}}
    result = opener.post(resource='nsfeature',
                         post_data=post_data, action='enable')
    logger.debug('configure_features result %s' % result)
    if result['nitro_errorcode'] == 0 or result['nitro_errorcode'] is None:
        logger.info('SUCCESS: Added NS Features {} to {}'.format(
            str(featurelist), opener.nsip))
    else:
        raise Exception('FAIL: Could not NS Features {} to {}'.format(
            str(featurelist), opener.nsip))


def save_config(opener):
    post_data = {
        'nsconfig': {}
    }
    result = opener.post(resource='nsconfig',
                         post_data=post_data, action='save')
    logger.debug('save_config result %s' % result)
    if result['nitro_errorcode'] == 0 or result['nitro_errorcode'] is None:
        logger.info('SUCCESS: Config saved for {}'.format(opener.nsip))
    else:
        raise Exception(
            'FAIL: Could not save config for {}'.format(opener.nsip))


# def ha_node_exists(opener, id):
#     result = opener.get(resource='hanode', id=id)
#     if result['nitro_errorcode'] == 258:
#         return False
#     elif result['nitro_errorcode'] == 0:
#         return True
#     else:
#         logger.info('ha_node_exists result %s' % result)
#         raise Exception('Failure to get ha node')


def add_ha_node(opener, ipaddress):
    post_data = {
        'hanode': {
            'id': '1',
            'inc': 'ENABLED',
            'ipaddress': ipaddress,
        }
    }
    result = opener.post(resource='hanode', post_data=post_data)
    logger.debug('add_ha_node result {}'.format(result))
    if result['nitro_errorcode'] == 0 or result['nitro_errorcode'] is None:
        logger.info('SUCCESS: HA node added for {}'.format(opener.nsip))
    else:
        raise Exception(
            'FAIL: Could not add HA node for {}'.format(opener.nsip))


# def vip_exists(opener, ipaddress):
#     result = opener.get(resource='nsip', args={'ipaddress': ipaddress})
#     logger.info(result)
#     if result['nitro_errorcode'] == 258:
#         return False
#     elif result['nitro_errorcode'] == 0:
#         return True
#     else:
#         logger.error('Cannot parse nitro_errorcode result: %s' % result)


def add_vip(opener, ipaddress, subnetmask):
    post_data = {
        'nsip': {
            'ipaddress': ipaddress,
            'netmask': subnetmask,
            'type': 'VIP',
        }
    }
    result = opener.post(post_data=post_data, resource='nsip')
    logger.debug('add_vip result %s' % result)
    if result['nitro_errorcode'] == 0 or result['nitro_errorcode'] is None:
        logger.info('SUCCESS: VIP added for {}'.format(opener.nsip))
    else:
        raise Exception('FAIL: Could not add VIP for {}'.format(opener.nsip))


# def remove_vip(opener, ipaddress):
#     result = opener.delete(resource='nsip', id=ipaddress)
#     if result['nitro_errorcode'] == 0:
#         logger.info('SUCCESS: VIP removed for {}'.format(ipaddress))
#     else:
#         logger.error('FAIL: Could not remove VIP for {}'.format(ipaddress))
#     logger.debug('remove_vip result %s' % result)


# def ipset_exists(opener, name):
#     result = opener.get(resource='ipset', id=name)
#     logger.info('ipset_exists result %s' % result)
#     if result['nitro_errorcode'] == 258:
#         return False
#     elif result['nitro_errorcode'] == 0:
#         return True
#     else:
#         logger.error('Unexpected ipset exists result %s' % result)
#         raise Exception()


def add_ipset(opener, name):
    post_data = {
        'ipset': {
            'name': name,
        }
    }
    result = opener.post(post_data=post_data, resource='ipset')
    logger.debug('add_ipset result %s' % result)
    if result['nitro_errorcode'] == 0 or result['nitro_errorcode'] is None:
        logger.info('SUCCESS: IPSET {} added for {}'.format(name, opener.nsip))
    else:
        raise Exception(
            'FAIL: Could not add IPSET {} for {}'.format(name, opener.nsip))


# def remove_ipset(opener, name):
#     result = opener.delete(resource='ipset', id=name)
#     logger.info('remove_ipset result: %s' % result)


# def remove_ha_node(opener, id):
#     result = opener.delete(resource='hanode', id=id)
#     logger.info('remove_ha_node result %s' % result)


def bind_ipset(opener, name, ipaddress):
    put_data = {
        'ipset_nsip_binding': {
            'name': name,
            'ipaddress': ipaddress,
        }
    }
    result = opener.put(put_data=put_data,
                        resource='ipset_nsip_binding', id=name)
    logger.debug('bind_ipset result: %s' % result)
    if result['nitro_errorcode'] == 0:
        logger.info('SUCCESS: {} is bound to IPSET {} in {}'.format(
            ipaddress, name, opener.nsip))
    else:
        raise Exception('FAIL: Could not bind {} to IPSET {} in {}'.format(
            ipaddress, name, opener.nsip))


# def unbind_ipset(opener, name, ipaddress):
#     result = opener.delete(resource='ipset_nsip_binding',
#                            id=name, args={'ipaddress': ipaddress})
#     logger.info('unbind_ipset result: %s' % result)
#     if result['nitro_errorcode'] != 0:
#         logger.error('unbind_ipset error %s' % result)
#         raise Exception()


# def ipset_binding_exists(opener, name, ipaddress):
#     args = {
#         'name': name,
#     }
#     result = opener.get(resource='ipset_nsip_binding', id=name)
#     logger.info('ipset_binding_exists result: %s' % result)


def lb_vserver_exists(opener, name):
    result = opener.get(resource='lbvserver', args={'name': name})
    logger.debug('lb_vserver_exists result: %s' % result)
    if result['nitro_errorcode'] == 0:
        return True
    else:
        return False


def add_lb_vserver(opener, name, ipaddress):
    post_data = {
        'lbvserver': {
            'name': name,
            'ipv46': ipaddress,
            'servicetype': 'HTTP',
            'port': 80,
            'ipset': 'ipset123',
        }
    }
    result = opener.post(resource='lbvserver', post_data=post_data)
    logger.debug('add_lb_vserver result: %s' % result)
    if result['nitro_errorcode'] == 0 or result['nitro_errorcode'] is None:
        logger.info(
            'SUCCESS: LB-Vserver {} added to {}'.format(name, ipaddress))
    else:
        raise Exception(
            'FAIL: Could not add LB-Vserver {} to {}'.format(name, ipaddress))


# def remove_lb_vserver(opener, name):
#     result = opener.delete(resource='lbvserver', id=name)
#     logger.info('remove_lb_vserver result %s' % result)


def lambda_handler(event, context):
    MAX_RETRIES = 40
    logger.info("event: {}".format(str(event)))
    request_type = event['RequestType']
    response_status = 'SUCCESS'
    # waitfor(25, reason='EC2 Instances status checks to pass')
    try:
        if request_type == 'Create':
            primary_instance_id = event['ResourceProperties']['PriInstanceID']
            primary_nsip = event['ResourceProperties']['PriNSIP']
            primary_vip = event['ResourceProperties']['PriVIP']
            primary_vip_subnet = event['ResourceProperties']['PriVIPSubnet']

            secondary_instance_id = event['ResourceProperties']['SecInstanceID']
            secondary_nsip = event['ResourceProperties']['SecNSIP']
            secondary_vip = event['ResourceProperties']['SecVIP']

            primary_nsip_pass = primary_instance_id
            secondary_nsip_pass = secondary_instance_id

            primary = NitroAPIOpener(
                nitro_protocol='https',
                nsip=primary_nsip,
                nitro_user='nsroot',
                nitro_pass=primary_nsip_pass,
                instance_id=primary_instance_id,
            )

            secondary = NitroAPIOpener(
                nitro_protocol='https',
                nsip=secondary_nsip,
                nitro_user='nsroot',
                nitro_pass=secondary_nsip_pass,
                instance_id=secondary_instance_id,
            )

            # Check if the reachability status is "passed" for both the instances
            retries = 1
            while retries <= MAX_RETRIES:
                if "passed" == primary.reachability_status() and \
                        "passed" == secondary.reachability_status():
                    logger.info(
                        'Primary and Secondary VPX instances reachability status passed')
                    break
                else:
                    waitfor(
                        5, "Rechabiliy status is not passed yet. Try No.{}".format(retries))
                    retries += 1

            try:  # If any of the following step fails, raise exception and return FAILED
                add_ha_node(primary, secondary_nsip)
                add_ha_node(secondary, primary_nsip)

                # Wait for the password to sync into Secondary-VPX.
                waitfor(
                    30, reason='secondary VPX password to get synced to that of primary')

                # From now, the Secondary-VPX password will be that of Primary-VPX
                secondary = NitroAPIOpener(
                    nitro_protocol='https',
                    nsip=secondary_nsip,
                    nitro_user='nsroot',
                    nitro_pass=primary_nsip_pass,
                    instance_id=secondary_instance_id,
                )

                add_ipset(primary, 'ipset123')
                add_ipset(secondary, 'ipset123')

                subnetmask = get_subnet_mask([primary_vip_subnet])
                add_vip(primary, secondary_vip, subnetmask)
                # add_vip(secondary, secondary_vip)

                bind_ipset(primary, 'ipset123', secondary_vip)
                bind_ipset(secondary, 'ipset123', secondary_vip)

                add_lb_vserver(primary, 'sample_lb_vserver', primary_vip)

                if lb_vserver_exists(secondary, 'sample_lb_vserver'):
                    logger.info('SUCCESS: {} and {} configured in HA mode'.format(
                        primary.nsip, secondary.nsip))
                else:
                    logger.error('FAIL: Could not configure {} and {} in HA mode'.format(
                        primary.nsip, secondary.nsip))

                configure_features(
                    primary, ['LB', 'CS', 'SSL', 'WL', 'CR', 'GSLB'])
                configure_features(
                    secondary, ['LB', 'CS', 'SSL', 'WL', 'CR', 'GSLB'])

                save_config(primary)
                save_config(secondary)

                response_status = 'SUCCESS'

            except Exception as e:
                logger.error('Failed to create custom resource ' + event['LogicalResourceId'] + ' in ' +
                event['StackId'] + ' in response to ' + event['RequestId'] + ': ' + str(e))
                response_status = 'FAILED'

            finally:
                send_response(event, context, response_status, {})
        elif request_type == 'Delete':
            send_response(event, context, 'SUCCESS', {})
        elif request_type == 'Update':
            send_response(event, context, 'SUCCESS', {})
    except Exception as e:
            logger.error('Top level exception {}'.format(str(e)))
            send_response(event, context, 'FAILED', {})


if __name__ == '__main__':
    event = {}
    parser = argparse.ArgumentParser()

    parser.add_argument('--primary_instance_id')
    parser.add_argument('--primary_public_nsip')
    parser.add_argument('--primary_nsip')
    parser.add_argument('--primary_vip')
    parser.add_argument('--primary_vip_subnet')
    parser.add_argument('--secondary_instance_id')
    parser.add_argument('--secondary_public_nsip')
    parser.add_argument('--secondary_nsip')
    parser.add_argument('--secondary_vip')

    args = parser.parse_args()

    primary_instance_id = args.primary_instance_id
    primary_nsip_public_ip = args.primary_public_nsip
    primary_nsip = args.primary_nsip
    primary_vip = args.primary_vip
    primary_vip_subnet = args.primary_vip_subnet

    secondary_instance_id = args.secondary_instance_id
    secondary_nsip_public_ip = args.secondary_public_nsip
    secondary_nsip = args.secondary_nsip
    secondary_vip = args.secondary_vip

    primary_nsip_pass = primary_instance_id
    secondary_nsip_pass = secondary_instance_id

    event = {
        'ResourceProperties': {
            'PriInstanceID': primary_instance_id,
            'PriPubNSIP': primary_nsip_public_ip,
            'PriPasswd': primary_nsip_pass,
            'PriNSIP': primary_nsip,
            'PriVIP': primary_vip,
            'PriVIPSubnet': primary_vip_subnet,
            'SecInstanceID': secondary_instance_id,
            'SecPubNSIP': secondary_nsip_public_ip,
            'SecPasswd': secondary_nsip_pass,
            'SecNSIP': secondary_nsip,
            'SecVIP': secondary_vip,
        },
        'RequestType': 'Create',
    }

    lambda_handler(event, None)
