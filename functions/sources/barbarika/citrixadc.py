from .helpers import logger
from .httpnitro import HTTPNitro


class CitrixADC(HTTPNitro):
    def __init__(self, nsip, nsuser, default_password, new_password):
        super().__init__(nsip=nsip, nsuser=nsuser, nspass=default_password)

        self.change_password(new_password)
        self.set_cli_prompt(promptstring="%u@%s")
        self.save_config()

    # System
    def reboot(self, warm=True):
        data = {"reboot": {"warm": warm}}
        result = self.do_post(data=data)
        if result:
            logger.info("Successfully reboot {}".format(self.nsip))
        else:
            raise Exception("Could not reboot {}".format(self.nsip))

    def set_cli_prompt(self, promptstring):
        # %u@%s -> nsroot@Primary;
        data = {"systemparameter": {"promptstring": promptstring}}
        result = self.do_put(data=data)
        if result:
            logger.info("SUCCESS: Changed CLI prompt of {} to {}".format(self.nsip, promptstring))
        else:
            logger.error("FAIL: Could not change CLI prompt of {} to  {}".format(self.nsip, promptstring))

    def change_password(self, new_pass):
        # check for new_pass already updated
        current_password = self.nspass  # backup current password, incase change_password fails
        self.put_nspass(new_pass)
        logger.info(
            "Before changing the password of {} to {}, checking if the password is already updated".format(
                self.nsip, self.nspass
            )
        )
        conn_status, conn_errcode = self.check_connection()
        if conn_status:
            logger.info("Password already changed to {}".format(self.nspass))
            self.headers["X-NITRO-PASS"] = self.nspass
            return True
        else:
            self.put_nspass(current_password)
            # checking connection with current password (default password) to catch `1046` errorcode
            conn_status, conn_errcode = self.check_connection()
            if conn_errcode == 1046:  # Forced password change at first login
                logger.info("First login forced password change request. Changing password..")
                if self.check_connection(new_password=new_pass)[0]:
                    self.put_nspass(new_pass)
                    logger.info("SUCCESS: Forced password change successful at first login for {}".format(self.nsip))
                else:
                    self.put_nspass(current_password)
                    raise Exception(
                        "FAILURE: Forced password change failed at first login for {}. Check logs for more details".format(
                            self.nsip
                        )
                    )
            else:
                logger.info("Password has not been changed earlier, need to change it")
                # its a normal change_password request
                data = {"systemuser": {"username": self.nsuser, "password": new_pass,}}
                result = self.do_put(data=data)

                if result:
                    self.put_nspass(new_pass)
                    self.headers["X-NITRO-PASS"] = self.nspass
                    logger.info("Successfully changed password of {} to {}".format(self.nsip, new_pass))
                    return True
                else:
                    self.put_nspass(current_password)
                    logger.error("Could not change password of {} to {}".format(self.nsip, new_pass))
                    logger.error("Refer log file for more information")
                    raise Exception

    def change_rpcnode_password(self, nodeip, new_rpc_password, secure="YES"):
        data = {
            "nsrpcnode": {
                "ipaddress": nodeip,
                "password": new_rpc_password,
                "secure": secure,
            }
        }
        result = self.do_put(data=data)
        if result:
            logger.info("SUCCESS: Changed RPC Node password for {}".format(self.nsip))
        else:
            logger.error("FAIL: Could not change RPC Node password for {}".format(self.nsip))

    # NS
    def save_config(self):
        data = {"nsconfig": {}}
        result = self.do_post(data=data, action="save")
        if result:
            logger.info("Successfully saved nsconfig of {}".format(self.nsip))
        else:
            raise Exception("Could not save nsconfig of {}".format(self.nsip))

    def configure_features(self, featurelist):
        data = {"nsfeature": {"feature": featurelist}}
        result = self.do_post(data=data, action="enable")
        if result:
            logger.info("SUCCESS: Added NS Features {} to {}".format(str(featurelist), self.nsip))
        else:
            raise Exception("FAIL: Could not NS Features {} to {}".format(str(featurelist), self.nsip))

    def set_nsip_gui(self, gui="SECUREONLY"):
        data = {"nsip": { "ipaddress": self.nsip, "gui": gui }}
        result = self.do_put(data=data)
        if result:
            logger.info("SUCCESS: Set NSIP GUI to {} for {}".format(gui, self.nsip))
        else:
            logger.error("FAIL: Could not set NSIP GUI to {} for {}".format(gui, self.nsip))

    def add_nsip(self, ip, netmask, iptype):
        data = {"nsip": {"ipaddress": ip, "netmask": netmask, "type": iptype}}
        result = self.do_post(data=data)
        if result:
            logger.info("Successfully added NSIP {} with type {}".format(ip, iptype))
        else:
            logger.error("Could not add NSIP {} with type {}".format(ip, iptype))
            logger.error("Refer log file for more information")
            raise Exception

    def get_nsip(self):
        nsip_dict = {"NSIP": [], "VIP": [], "SNIP": []}
        result = self.do_get(resource="nsip")
        if result:
            for ip_dict in result["nsip"]:
                if ip_dict["type"] == "NSIP":
                    nsip_dict["NSIP"].append(ip_dict["ipaddress"])
                elif ip_dict["type"] == "VIP":
                    nsip_dict["VIP"].append(ip_dict["ipaddress"])
                elif ip_dict["type"] == "SNIP":
                    nsip_dict["SNIP"].append(ip_dict["ipaddress"])
        return nsip_dict

    def remove_nsip(self, ipaddress):
        result = None
        try:
            result = self.do_delete(resource="nsip", id=str(ipaddress))
        except Exception as e:
            logger.error("Unable to remove NSIP {}: Exception: {}".format(ipaddress, str(e)))
            return

        if result:
            logger.info("Successfully removed NSIP {}".format(ipaddress))
        else:
            logger.error("Could not remove NSIP {}".format(ipaddress))
            logger.error("Refer log file for more information")
            raise Exception

    # HA
    def add_hanode(self, id, ipaddress, incmode):
        data = {"hanode": {"id": id, "inc": "ENABLED" if incmode else "DISABLED", "ipaddress": ipaddress,}}
        result = self.do_post(data=data)
        if result:
            logger.info("SUCCESS: HA node added for {}".format(self.nsip))
        else:
            raise Exception("FAIL: Could not add HA node for {}".format(self.nsip))

    def hafailover(self, force=True):
        data = {"hafailover": {"force": force,}}
        result = self.do_post(data=data, action="Force")
        if result:
            logger.info("SUCCESS: Force HA failover for {}".format(self.nsip))
        else:
            raise Exception("FAIL: Could not force HA failover for {}".format(self.nsip))

    def is_primarynode(self):
        result = self.do_get(resource="hanode")
        if result:
            for node in result["hanode"]:
                if node["ipaddress"] != self.nsip:
                    continue
                return True if node["state"].upper() == "PRIMARY" else False
            else:
                raise Exception("Did not find {} in `show ha node`".format(self.nsip))
        else:
            raise Exception("show ha node exception {}".format(result))

    # Network

    def add_ipset(self, name):
        data = {"ipset": {"name": name,}}
        result = self.do_post(data=data)
        if result:
            logger.info("SUCCESS: IPSET {} added for {}".format(name, self.nsip))
        else:
            raise Exception("FAIL: Could not add IPSET {} for {}".format(name, self.nsip))

    def add_route(self, network_ip, netmask, gateway_ip):
        data = {"route": {"network": network_ip, "netmask": netmask, "gateway": gateway_ip,}}
        result = self.do_post(data=data)
        if result:
            logger.info('SUCCESS: "route {} {} {}" added to {}'.format(network_ip, netmask, gateway_ip, self.nsip))
        else:
            raise Exception(
                'FAIL: Could not add "route {} {} {}" to {}'.format(network_ip, netmask, gateway_ip, self.nsip)
            )

    def remove_route(self, network_ip, netmask, gateway_ip):
        # for remote_route: https://10.0.x.x/nitro/v1/config/route?args=network:0.0.0.0,netmask:0.0.0.0,gateway:10.0.13.1
        args = "network:{},netmask:{},gateway:{}".format(network_ip, netmask, gateway_ip)

        result = self.do_delete(resource="route", args=args)
        if result:
            logger.info('SUCCESS: "route {} {} {}" removed for {}'.format(network_ip, netmask, gateway_ip, self.nsip))
        else:
            raise Exception(
                'FAIL: Could not remove "route {} {} {}" for {}'.format(network_ip, netmask, gateway_ip, self.nsip)
            )

    def bind_ipset(self, name, ipaddress):
        data = {"ipset_nsip_binding": {"name": name, "ipaddress": ipaddress,}}
        result = self.do_put(data=data)
        if result:
            logger.info("SUCCESS: {} is bound to IPSET {} in {}".format(ipaddress, name, self.nsip))
        else:
            raise Exception("FAIL: Could not bind {} to IPSET {} in {}".format(ipaddress, name, self.nsip))

    # LB
    def add_lbvserver(self, name, servicetype, ipaddress, port, ipset=None):
        data = {
            "lbvserver": {
                "name": name,
                "ipv46": ipaddress,
                "servicetype": servicetype,
                "port": port,
                # 'ipset': ipset,
            }
        }
        if ipset:
            data["lbvserver"]["ipset"] = ipset

        result = self.do_post(data=data)
        if result:
            logger.info("SUCCESS: LB Vserver {} added to {}".format(name, self.nsip))
        else:
            raise Exception("FAIL: Could not add LB Vserver {} to {}".format(name, self.nsip))

    def get_lbvserver(self, name):
        return self.do_get(resource="lbvserver", id=name)

    def bind_lbvserver_service(self, lbvserver_name, servicename):
        data = {"lbvserver_service_binding": {"name": lbvserver_name, "servicename": servicename,}}
        result = self.do_put(data=data, id=lbvserver_name)
        if result:
            logger.info(
                "SUCCESS: lbvserver {} is bound to service {} in {}".format(lbvserver_name, servicename, self.nsip)
            )
        else:
            raise Exception(
                "FAIL: Could not bind lbvserver {} to service {} in {}".format(lbvserver_name, servicename, self.nsip)
            )

    def add_service(self, servicename, serviceip, servicetype, port):
        data = {"service": {"name": servicename, "ip": serviceip, "servicetype": servicetype, "port": port,}}
        result = self.do_post(data=data)
        if result:
            logger.info("SUCCESS: Service {} added to {}".format(servicename, self.nsip))
        else:
            raise Exception("FAIL: Could not add Service {} to {}".format(servicename, self.nsip))

    # Pooled License
    def add_licenseserver(self, admip, admport=27000):
        data = {
            "nslicenseserver": {
                # "servername": admip,
                "licenseserverip": admip,
                "port": admport,
            }
        }
        result = self.do_post(data=data)
        if result:
            logger.info("SUCCESS: License server {} added to {}".format(admip, self.nsip))
        else:
            raise Exception("FAIL: Could not add licenseserver {} to {}".format(admip, self.nsip))

    def allocate_pooled_license(self, licensingmode, bandwidth, pooled_edition, platform, cpu_edition):
        platform_map = {
            "VPX-10": "VP10",
            "VPX-25": "VP25",
            "VPX-200": "VP200",
            "VPX-1000": "VP1000",
            "VPX-3000": "VP3000",
            "VPX-5000": "VP5000",
            "VPX-8000": "VP8000",
            "VPX-10G": "VP10000",
            "VPX-15G": "VP15000",
            "VPX-25G": "VP25000",
            "VPX-40G": "VP40000",
            "VPX-100G": "VP100000",
        }

        # Mapping old way of license edition to new way of license edition
        if pooled_edition == "Advanced" or cpu_edition == "Advanced":
            edition = "Enterprise"
        elif pooled_edition == "Premium" or cpu_edition == "Premium":
            edition = "Platinum"
        else:
            edition = "Standard"

        data = {}
        if licensingmode == "CICO-Licensing":
            try:
                data = {"nscapacity": {"platform": platform_map[platform]}}
            except KeyError as e:
                raise Exception("FAIL: {}".format(str(e)))
        elif licensingmode == "Pooled-Licensing":
            data = {"nscapacity": {"bandwidth": bandwidth, "edition": edition, "unit": "Mbps",}}
        elif licensingmode == "CPU-Licensing":
            data = {"nscapacity": {"vcpu": True, "edition": edition}}
        result = self.do_put(data=data)
        if result:
            logger.info("SUCCESS: Allocated {} Mbps to {} in {} edition".format(bandwidth, self.nsip, edition))
        else:
            raise Exception("FAIL: Could not allocate license")

    def get_pooled_license(self):
        return self.do_get(resource="nscapacity")["nscapacity"]

    def validate_pooled_license(self, licensingmode, bandwidth, pooled_edition, platform, cpu_edition):
        nscapacity = self.get_pooled_license()
        """
        nscapacity = {
            "actualbandwidth": "100",
            "maxvcpucount": "4",

            "edition": "Platinum",
            "unit": "Mbps",
            "bandwidth": "100",

            "maxbandwidth": "100000",
            "minbandwidth": "10",
            "instancecount": "1"
        }
        nscapacity=  {
            "nodeid":<Double_value>,
            "actualbandwidth":<Double_value>,

            "platform":<String_value>,

            "vcpucount":<Double_value>,
            "maxvcpucount":<Double_value>,

            "edition":<String_value>,
            "unit":<String_value>,
            "bandwidth":<Double_value>,
            "maxbandwidth":<Double_value>,
            "minbandwidth":<Double_value>,

            "instancecount":<Double_value>
        }
        """
        # Mapping old way of license edition to new way of license edition
        edition_map = {
            # new_edition_name: old_edition_name
            "Premium": "Platinum",
            "Advanced": "Enterprise",
        }

        if licensingmode == "CICO-Licensing":
            # platform
            logger.info("SUCCESS: TODO: Returning SUCCESS without validation for {}".format(self.nsip))
            return True

        elif licensingmode == "Pooled-Licensing":
            # bandwidth, edition, unit
            # Assuming unit to be in Mbps, as allocation happened in Mbps
            # TODO: take care of Gbps unit if necessary
            if nscapacity["bandwidth"] == bandwidth and nscapacity["edition"] == edition_map[pooled_edition]:
                logger.info("SUCCESS: Validation of pooled license is successful for {}".format(self.nsip))
                return True
        elif licensingmode == "CPU-Licensing":
            # vcpu, edition
            logger.info("SUCCESS: TODO: Returning SUCCESS without validation for {}".format(self.nsip))
            return True
        raise Exception("FAIL: Pooled license allocation validation failed for {}".format(self.nsip))

    # AppFW
    def check_license(self, nsfeature):
        result = self.do_get(resource="nslicense")
        return True if result["nslicense"][nsfeature] else False

    def add_appfw_profile(self, profilename, configdict={}):
        data = {"appfwprofile": {"name": profilename,}}
        data["appfwprofile"].update(configdict)
        result = self.do_post(data=data)
        if result:
            logger.info("SUCCESS: AppFw Profile {} added for {}".format(profilename, self.nsip))
        else:
            raise Exception("FAIL: Could not add AppFw Profile {} for {}".format(profilename, self.nsip))

    def add_appfw_policy(self, policyname, profilename, rule):
        data = {"appfwpolicy": {"name": policyname, "profilename": profilename, "rule": rule,}}
        result = self.do_post(data=data)
        if result:
            logger.info("SUCCESS: AppFw Policy {} added for {}".format(policyname, self.nsip))
        else:
            raise Exception("FAIL: Could not add AppFw Policy {} for {}".format(policyname, self.nsip))

    def bind_appfw_global_policy(self, policyname, priority, type):
        data = {"appfwglobal_appfwpolicy_binding": {"policyname": policyname, "priority": priority, "type": type,}}
        result = self.do_put(data=data)
        if result:
            logger.info("SUCCESS: AppFw policy {} is bound GLOBALLY in {}".format(policyname, self.nsip))
        else:
            raise Exception("FAIL: Could not bind AppFw policy {} GLOBALLY in {}".format(policyname, self.nsip))

    # Cluster
    def get_clip(self):
        result = self.do_get(resource="nsip")
        if result:
            for ip_dict in result["nsip"]:
                if ip_dict["type"] == "CLIP":
                    return ip_dict["ipaddress"]
            return False  # No CLIP found

    def add_clusterinstance(self, instID):
        data = {"clusterinstance": {"clid": str(instID),}}
        result = self.do_post(data=data)
        if result:
            logger.info("Successfully added cluster instance {} to {}".format(instID, self.nsip))
        else:
            logger.error("Could not add cluster instance {} to {}".format(instID, self.nsip))
            logger.error("Refer log file for more information")
            raise Exception

    def enable_clusterinstance(self, instID):
        data = {"clusterinstance": {"clid": str(instID),}}
        result = self.do_post(data=data, action="enable")
        if result:
            logger.info("Successfully enabled cluster instance {} to {}".format(instID, self.nsip))
        else:
            logger.error("Could not enabled cluster instance {} to {}".format(instID, self.nsip))
            logger.error("Refer log file for more information")
            raise Exception

    def add_clusternode(self, nodeID, nodeIP, backplane, tunnelmode, state):
        data = {
            "clusternode": {
                "nodeid": str(nodeID),
                "ipaddress": nodeIP,
                "state": state,
                "backplane": backplane,
                "tunnelmode": tunnelmode,
            }
        }
        result = self.do_post(data=data)
        if result:
            logger.info("Successfully added cluster node with ID:{} and nodeIP:{}".format(nodeID, nodeIP))
        else:
            logger.error("Could not add cluster node with ID:{} and nodeIP:{}".format(nodeID, nodeIP))
            logger.error("Refer log file for more information")
            raise Exception

    def set_clusternode(self, nodeID, state):
        data = {"clusternode": {"nodeid": str(nodeID), "state": state,}}
        result = self.do_put(data=data)
        if result:
            logger.info("Successfully set cluster node {} to state {}".format(nodeID, state))
        else:
            logger.error("Could not add cluster node {} to state {}".format(nodeID, state))
            logger.error("Refer log file for more information")
            raise Exception

    def remove_clusternode(self, nodeID):
        result = None
        try:
            result = self.do_delete(resource="clusternode", id=str(nodeID))
        except Exception as e:
            logger.error("Unable to fetch response from the CLIP. Reason:{}".format(str(e)))
            return

        if result:
            logger.info("Successfully removed cluster node {}".format(nodeID))
        else:
            logger.error("Could not remove cluster node {}".format(nodeID))
            logger.error("Refer log file for more information")
            raise Exception

    def join_cluster(self, clip, password):
        data = {"cluster": {"clip": clip, "password": password}}
        result = self.do_post(data=data, action="join")
        if result:
            logger.info("Successfully joined cluster node {}".format(self.nsip))
        else:
            logger.error("Could not join cluster node {}".format(self.nsip))
            logger.error("Refer log file for more information")
            raise Exception
