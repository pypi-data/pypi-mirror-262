import json
from tools.feature_template_payload import FeatureTemplatePayload as PAYLOAD

class AdministrationTenantManagement():

    def administration_tenantManagementTenants_addTenant(self, payload, success_analyze=False):
        """
        UI(20.9):
            UI: Administration -> Tenant Management -> Tenants -> Add Tenant -> New Tenant

        payload = [
                    {
                        "orgName": "st-regression-Orange Inc",
                        "subDomain": "orange.mtreg.com",
                        "name": "Orange Inc",
                        "desc": "Orange Inc Tenant",
                        "wanEdgeForecast": 100
                    }
                ]
        # after 20.6, this is added
        payload['wanEdgeForecast'] = 100

        success:
            ret.status_code: 200
            ret.text: {"id":"16a85afc-dd0b-4137-a8e8-50c9a258ce6a"}
        """
        api = '/dataservice/tenant/bulk/async'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("POST", url, data=json.dumps(payload))
        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()["id"]]

    def administration_tenantManagementTenants_Tenants_GET(self, success_analyze=False):
        """
        UI(20.12):
            UI: Administration -> Tenant Management -> Tenants -> refresh button

        success:
            ret.status_code: 200
            ret.text: api_data/administration_tenantManagementTenants_Tenants_GET.log
        """
        api = '/dataservice/tenant'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)
        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()["data"]]

    def administration_tenantManagement_ResourceProfile(self, resource_pf_dict, success_analyze=False):
        """
        UI(20.12):
            UI: Administration -> Tenant Management -> Resource Profile -> Add Resource Profile

        success:
            ret.status_code: 200
            ret.text: '"OK"'
        """
        api = "/dataservice/device/tier"
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)

        payload = PAYLOAD.tenant_resource_profile_payload()
        payload["tierName"] = resource_pf_dict['name']

        if 'max_vpn' in resource_pf_dict.keys():
            payload["vpn"] = resource_pf_dict['max_vpn']

        if 'color' in resource_pf_dict.keys():
            c_list = [resource_pf_dict['color']] if not isinstance(resource_pf_dict['color'], list) else resource_pf_dict['color']
            payload["tlocs"] = []
            for color in c_list:
                payload["tlocs"].append(
                    {
                        "color": color,
                        "encapsulation": "ipsec"
                    }
                )
        
        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()]

    def administration_tenantManagement_ResourceProfile_GET(self, success_analyze=False):
        """
        UI(20.12):
            UI: Administration -> Tenant Management -> Resource Profile

        success:
            ret.status_code: 200
            ret.text: api_data/administration_tenantManagementTenants_ResourceProfile_GET.log
        """
        api = "/dataservice/device/tier"
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]

