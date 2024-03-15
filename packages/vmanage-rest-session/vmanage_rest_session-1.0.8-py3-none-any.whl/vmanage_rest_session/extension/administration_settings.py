import json
class AdministrationSettings():

    def administration_settings_organization_name_set(self, org_name, domain_id=1, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Administration -> Settings -> SP Organization Name(MT)/Organization Name(ST)
            UI value:
                Organization: org_name
        success:
            ret.status_code: 200
            ret.text: '{"data":[{"domain-id":"1","org":"st-regression"}]}'
        """
        api = '/dataservice/settings/configuration/organization'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        payload = {"domain-id": "{}".format(domain_id), "org": "{}".format(org_name)}
        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret]

    def administration_settings_organization_name_get(self, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Administration -> Settings -> SP Organization Name(MT)/Organization Name(ST) -> refresh
        success:
            ret.status_code: 200
            ret.text: '{"data":[{"domain-id":"1","org":"vIPtela Inc Regression","controlConnectionUp":true}]}'
        """
        api = '/dataservice/settings/configuration/organization'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()["data"]]

    def administration_settings_vbond_set(self, vbond_ip_dns_name, port=12346, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Administration -> Settings -> vBond
            UI value:
                vBond DNS/ IP Address: payload

        success:
            ret.status_code: 200
            ret.text: '{"data":[{"domainIp":"10.0.44.13","port":"12346"}]}'
        """
        api = '/dataservice/settings/configuration/device'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        payload = {"domainIp": vbond_ip_dns_name, "port": "{}".format(port)}
        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret]

    def administration_settings_vbond_get(self, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Administration -> Settings -> vBond -> refresh

        success:
            ret.status_code: 200
            ret.text: '{"data":[{"domainIp":"vbond","port":"12346"}]}'
        """
        api = '/dataservice/settings/configuration/device'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()["data"]]

    # There are some issue, will be changd later
    # def administration_manageUsers_users_changePassword(self, user, password, success_analyze=False):
    #     """
    #     Same Effect to UI(20.9):
    #         UI: Administration -> Manage Users -> Users -> user(admin) -> Change Password
    #         UI API: /dataservice/admin/user/password/admin
    #         UI Payload: {"locale":"en_US","currentPassword":false,"showPassword":false,"showConfirmPassword":false,"userName":"admin","currentUserPassword":"xxxxx","password":"Login_999"}
    #     success:
    #         ret.status_code: 200
    #         ret.text: 
    #     """
    #     api = '/dataservice/admin/user/password/{}'.format(user)
    #     payload = {'userName': user, 'password': password}
    #     url = 'https://{}:{}{}'.format(self.ip, self.port, api)
    #     ret = self.http_request("PUT", url=url, data=json.dumps(payload))

    #     if not success_analyze:
    #         return ret

    #     if ret.status_code != 200:
    #         return [False, ret]
    #     else:
    #         return [True, ret]

    def administration_settings_tenancyMode_multitenant_set(self, domain="fruits.com", clusterid="", success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Administration -> Settings -> Controllers -> Tenancy Mode -> Multitenant
            UI value: 
                Domain: domain
                clusterid: Cluster Id
        Local File Changed To:
            MT1_vmanage1:~# cat /opt/web-app/etc/deployment
            #Last modified by app-server.
            #Wed Apr 12 08:06:11 UTC 2023
            deploymentmode=Cluster
            tenantmode=MultiTenant
            domain=mtregr.com
            clusterid=na0
            MT1_vmanage1:~#
        Impact:
            Application Server will reboot, vmanage api access will return status_code 503
        Success:
            ret.status_code: 200
            ret.text: '{}'
        Fail:
            ret.status_code: 400
            ret.text: '{"error":{"type":"error","message":"Failed to change tenant mode changes","details":"Cannot change tenant mode for vManage having connected devices","code":"VCC0027"}}'
        """
        api = '/dataservice/clusterManagement/tenancy/mode'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        payload = {'mode': 'MultiTenant', 'domain': domain}

        if clusterid:
            payload["clusterid"] = clusterid

        ret = self.http_request("POST", url=url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret]

    def administration_settings_tenancyMode_multitenant_get(self, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Administration -> Settings -> Controllers -> Tenancy Mode -> Multitenant -> refresh
        Success:
            ret.status_code: 200
            ret.text: {
                "header":
                {
                    "generatedOn": 1683702273695
                },
                "data":
                {
                    "mode": "MultiTenant",
                    "domain": "fruits.com",
                    "clusterid": "",
                    "deploymentmode": "Cluster"
                }
            }
        """
        api = '/dataservice/clusterManagement/tenancy/mode'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)

        ret = self.http_request("GET", url=url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()["data"]]
    
    def administration_settings_mt_edge_deployment_set(self, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Administration -> Settings -> MT Edge Deployment Settings
        success:
            ret.status_code: 200
            ret.text: '{"data":[{"mtEdgeDeploy":true}]}'
        """
        api = '/dataservice/settings/configuration/mtEdgeDeployment'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        payload = {"mtEdgeDeploy": True}
        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret]
    
    def administration_settings_mt_edge_deployment_get(self, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Administration -> Settings -> MT Edge Deployment Settings -> refresh
        success:
            ret.status_code: 200
            ret.text: '{"data":[{"mtEdgeDeploy":false}]}'
        """
        api = '/dataservice/settings/configuration/mtEdgeDeployment'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)

        ret = self.http_request("GET", url=url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()["data"]]

