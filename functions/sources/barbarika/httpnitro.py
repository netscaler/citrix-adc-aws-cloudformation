import json
import requests
from .helpers import logger


class HTTPNitro:
    def __init__(
        self, nsip, nsuser, nspass, nitro_protocol="https", ns_api_path="nitro/v1/config",
    ):
        self.nitro_protocol = nitro_protocol
        self.api_path = ns_api_path
        self.nsip = nsip
        self.nsuser = nsuser
        self.nspass = nspass
        self.ssl_verify = False  # FIXME: validate Certificate

        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.headers["X-NITRO-USER"] = self.nsuser
        self.headers["X-NITRO-PASS"] = self.nspass

    # Do not directly update nspass or other class variables. use these functions
    def put_nspass(self, new_nspass):
        logger.info("put_nspass: changing self.nspass from {} to {}".format(self.nspass, new_nspass))
        self.nspass = new_nspass
        self.headers["X-NITRO-PASS"] = new_nspass

    def construct_url(self, resource, id=None, action=None, args=None):
        # Construct basic get url
        url = "%s://%s/%s/%s" % (self.nitro_protocol, self.nsip, self.api_path, resource,)

        # Append resource id
        if id is not None:
            url = "%s/%s" % (url, id)

        # Append action
        if action is not None:
            url = "%s?action=%s" % (url, action)
        elif args is not None:
            url = "%s?args=%s" % (url, args)

        return url

    def check_connection(self, new_password=None):
        """
        Return: tuple(<True/False>, <errorcode>)
            errorcodes:
                -1 : Node not reachable
                0 : Success login
                response['errorcode'] : NITRO errorcode
        """
        url = self.construct_url(resource="login")

        headers = {}
        headers["Content-Type"] = "application/json"
        payload = {"login": {"username": self.nsuser, "password": self.nspass}}
        if new_password is not None:
            payload["login"]["new_password"] = new_password

        try:
            logger.debug("post_data: {}".format(json.dumps(payload, indent=4)))
            logger.debug("HEADERS: {}".format(json.dumps(self.headers, indent=4)))
            r = requests.post(url=url, headers=headers, json=payload, verify=self.ssl_verify)
            response = r.json()
            logger.debug("do_login response: {}".format(json.dumps(response, indent=4)))
            if response["severity"] == "ERROR":
                logger.error(
                    "Could not login to {} with user:{} and passwd:{}".format(self.nsip, self.nsuser, self.nspass)
                )
                logger.error("{}: {}".format(response["errorcode"], response["message"]))
                return (False, response["errorcode"])
            return (True, 0)
        except Exception as e:
            logger.error("Node {} is not reachable. Reason:{}".format(self.nsip, str(e)))
            return (False, -1)

    def do_get(self, resource, id=None, action=None):
        url = self.construct_url(resource, id, action)
        logger.debug("GET {}".format(url))
        logger.debug("HEADERS: {}".format(json.dumps(self.headers, indent=4)))

        r = requests.get(url=url, headers=self.headers, verify=self.ssl_verify,)
        if r.status_code == 200:
            response = r.json()
            logger.debug("do_get response: {}".format(json.dumps(response, indent=4)))
            return response
        else:
            logger.error("GET failed: {}".format(r.text))
            return False

    def do_post(self, data, id=None, action=None):
        resource = list(data)[0]
        url = self.construct_url(resource, id, action)
        logger.debug("POST {}".format(url))
        logger.debug("POST data: {}".format(json.dumps(data, indent=4)))
        logger.debug("HEADERS: {}".format(json.dumps(self.headers, indent=4)))

        r = requests.post(url=url, headers=self.headers, json=data, verify=self.ssl_verify)
        # print(r.text)
        logger.info(r.status_code)
        if r.status_code == 201 or r.status_code == 200:
            return True
        else:
            logger.error("POST failed: {}".format(r.text))
            return False

    def do_put(self, data, id=None, action=None):
        resource = list(data)[0]
        url = self.construct_url(resource, id, action)
        logger.debug("PUT {}".format(url))
        logger.debug("PUT data: {}".format(json.dumps(data, indent=4)))
        logger.debug("HEADERS: {}".format(json.dumps(self.headers, indent=4)))

        r = requests.put(url=url, headers=self.headers, json=data, verify=self.ssl_verify)
        if r.status_code == 201 or r.status_code == 200:
            return True
        else:
            logger.error("PUT failed: {}".format(r.text))
            return False

    def do_delete(self, resource, id=None, action=None, args=None):
        url = self.construct_url(resource, id, action, args)
        logger.debug("DELETE {}".format(url))
        logger.debug("HEADERS: {}".format(json.dumps(self.headers, indent=4)))

        r = requests.delete(url=url, headers=self.headers, verify=self.ssl_verify)
        # response = r.json()
        # logger.debug("do_delete response: {}".format(
        #     json.dumps(response, indent=4)))
        if r.status_code == 200:
            return True
        else:
            logger.error("DELETE failed: {}".format(r.text))
            return False
