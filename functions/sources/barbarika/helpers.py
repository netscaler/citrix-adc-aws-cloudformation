import json
import logging
import time
import sys
import ipaddress

if sys.version_info[0] != 3:
    raise Exception("Can only run under python3")

LOGFILE = __file__ + ".log"
formatter = logging.Formatter("%(asctime)s: %(levelname)s - %(message)s")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


def waitfor(seconds=2, reason=None):
    if reason is not None:
        logger.info("Waiting for {} seconds. Reason: {}".format(seconds, reason))
    else:
        logger.info("Waiting for {} seconds".format(seconds))
    time.sleep(seconds)


# def to_json(data):
#     return codecs.encode(json.dumps(data))


def to_json(data, indent=2):
    return json.dumps(data, indent=indent)


def from_json(data):
    return json.loads(data)


def get_gateway_ip(cidr):
    return [str(ip) for ip in ipaddress.IPv4Network(cidr)][1]


def cidr_to_netmask(cidr):
    return (str(ipaddress.IPv4Network(cidr).network_address), str(ipaddress.IPv4Network(cidr).netmask))
