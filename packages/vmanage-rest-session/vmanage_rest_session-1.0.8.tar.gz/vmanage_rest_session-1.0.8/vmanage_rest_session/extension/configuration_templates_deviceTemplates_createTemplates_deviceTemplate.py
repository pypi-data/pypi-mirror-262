import json
import time
import copy
from tools.feature_template_payload import FeatureTemplatePayload as PAYLOAD

class ConfigurationTemplatesDeviceTemplate():
    def configuration_templates_deviceTemplates_featureTemplates_system(self, template_name, device_type, site_id, template_dscp=None, success_analyze=False):
        """
        Equal to UI(20.12):
            UI: Configuration -> Templates -> Feature Templates -> Add Template 
        success:
            ret.status_code: 200
            ret.text: '{"templateId":"a384fb78-54ad-4c96-96cc-1cdfd0c46c40"}'
        """
        api = "/dataservice/template/feature/"
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)

        payload = PAYLOAD.cisco_system_payload()
        payload["templateName"] = template_name
        payload["templateDescription"] = template_name if template_dscp is None else template_dscp
        payload["deviceType"].append(device_type)
        payload["templateDefinition"]["site-id"]["vipValue"] = site_id

        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()["templateId"]]
    
    def configuration_templates_deviceTemplates_featureTemplates_tenant(self, template_name, device_type, tenant_dict, template_dscp=None, success_analyze=False):
        """
        Equal to UI(20.12):
            UI: Configuration -> Templates -> Feature Templates -> Add Template -> Tenant
        success:
            ret.status_code: 200
            ret.text: '{"templateId":"a384fb78-54ad-4c96-96cc-1cdfd0c46c40"}'
        """
        api = "/dataservice/template/feature/"
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)

        payload = PAYLOAD.cisco_tenant_payload()
        payload["templateName"] = template_name
        payload["templateDescription"] = template_name if template_dscp is None else template_dscp
        payload["deviceType"].append(device_type)

        for tenant in tenant_dict.values():
            sub_payload = PAYLOAD._cisco_tenant_payload()
            sub_payload["org-name"]["vipValue"] = tenant['orgName']
            sub_payload["universal-unique-id"]["vipValue"] = tenant['unique_id']
            sub_payload["global-tenant-id"]["vipValue"] = tenant['global_tenant_id']
            sub_payload["tier"]["tier-name"]["vipValue"] = tenant['pf']["name"]
            if 'max_vpn' in tenant['pf'].keys():
                sub_payload["tier"]["max-vpn"]["vipValue"] = tenant['pf']["max_vpn"]
            
            if 'color' in tenant['pf'].keys():
                c_list = [tenant['pf']['color']] if not isinstance(tenant['pf']['color'], list) else tenant['pf']['color']
                sub_payload["tenant-tloc"]["vipValue"] = []
                for each_color in c_list:
                    sub_sub_payload = PAYLOAD._cisco_tenant_tloc_payload()
                    sub_sub_payload["color"]["vipValue"] = each_color
                    sub_payload["tenant-tloc"]["vipValue"].append(sub_sub_payload)

            payload['templateDefinition']['tenant']['vipValue'].append(sub_payload)

        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret.text]
        else:
            return [True, ret.json()["templateId"]]

    def configuration_templates_deviceTemplates_featureTemplates_vpn(self, template_name, device_type, vpn_id, template_dscp=None, success_analyze=False, kwargs={}):

        """
        kwargs:
            {'default_gateway': '', 'tenant': '', 'ip_host': ''} 
        Equal to UI(20.12):
            UI: Configuration -> Templates -> Feature Templates -> Add Template -> Cisco Vpn
        success:
            ret.status_code: 200
            ret.text: '{"templateId":"a384fb78-54ad-4c96-96cc-1cdfd0c46c40"}'
        """
        api = "/dataservice/template/feature/"
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)

        payload = PAYLOAD.cisco_vpn_payload()
        vpn_key = 'tenant-vpn-id'
        if vpn_id == 0 or vpn_id ==512:
            payload["templateDefinition"].pop("tenant-vpn-id")
            payload["templateDefinition"].pop("org-name")
            vpn_key = 'vpn-id'
        else:
            payload["templateDefinition"]["org-name"]["vipValue"] = kwargs['tenant']
            payload["templateDefinition"]['vpn-id']["vipValue"] = self._get_device_vpn_for_tenant(kwargs['tenant'], vpn_id)
        payload["templateName"] = template_name
        payload["templateDescription"] = template_name if template_dscp is None else template_dscp
        payload["deviceType"].append(device_type)
        payload["templateDefinition"][vpn_key]["vipValue"] = vpn_id

        if kwargs.get('default_gateway'):
            payload["templateDefinition"]["ip"]["route"]["vipValue"][0]["next-hop"]["vipValue"][0]["address"]["vipValue"] = kwargs['default_gateway']
        else:
            payload["templateDefinition"]["ip"].pop("route")
        
        if kwargs.get('ip_host'):
            payload["templateDefinition"]["host"]["vipType"] = "constant"
            sub_payload = PAYLOAD._ip_host_payload()
            sub_payload["ip"]["vipValue"] = kwargs.get('ip_host')
            payload["templateDefinition"]["host"]["vipValue"].append(sub_payload)

        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()["templateId"]]

    def configuration_templates_deviceTemplates_featureTemplates_interface(self, template_name, device_type, ifname, intf_ip, template_dscp=None, success_analyze=False, kwargs={}):
        """
        kwargs:
            {'intf_tunnel': True} 
        Equal to UI(20.12):
            UI: Configuration -> Templates -> Feature Templates -> Add Template -> Cisco Vpn Ethernet Interface
        success:
            ret.status_code: 200
            ret.text: '{"templateId":"a384fb78-54ad-4c96-96cc-1cdfd0c46c40"}'
        """
        api = "/dataservice/template/feature/"
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)

        payload = PAYLOAD.cisco_vpn_interface_payload()
        payload["templateName"] = template_name
        payload["templateDescription"] = template_name if template_dscp is None else template_dscp
        payload["deviceType"].append(device_type)
        payload["templateDefinition"]["if-name"]["vipValue"] = ifname
        payload["templateDefinition"]["ip"]["address"]["vipValue"] = intf_ip + "/24"
        
        if not kwargs.get('intf_tunnel'):
            payload['templateDefinition'].pop("tunnel-interface")

        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()["templateId"]]

    def _get_device_vpn_for_tenant(self, tenant_org_name, tenant_vpn_id):
        '''
        This is the helper function of configuration_templates_deviceTemplates_featureTemplates_vpn.
        To get device vpn for a specified (tenant, tenant_id)
        '''
        api = '/dataservice/resourcepool/resource/vpn'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        payload = {'resourcePoolDataType': 'vpn', 'tenantId': tenant_org_name, 'tenantVpn': tenant_vpn_id}
        
        ret = self.http_request("PUT", url, data=json.dumps(payload))
        return ret.json()['deviceVpn']

    def configuration_templates_deviceTemplates_getAllFeatureTemplate(self, success_analyze=False):
        """
        Equal to UI(20.12):
            UI: Configuration -> Templates -> Feature Templates -> (Refresh Button)
        success:
            ret.status_code: 200
            ret.text: api_data/configuration_templates_deviceTemplates_getAllFeatureTemplate_GET_20.12.log
        """
        api = '/dataservice/template/feature/'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]
    
    def configuration_templates_getAllFeatureTemplateID_by_name(self):
        '''
        A helper funtion to format all feature templates by {name: feature_template_id}
        '''
        tmplName_tmplId_dict = {}
        ret = self.configuration_templates_deviceTemplates_getAllFeatureTemplate(success_analyze=True)
        for ft in ret[1]:
            tmplName_tmplId_dict.update(
                {
                    ft['templateName']: ft['templateId']
                }
            )
        
        return tmplName_tmplId_dict
    
    def configuration_templates_deviceTemplates_create_deviceTemplate(self, template_name, device_type, mtedge_ft_name_dict, ft_id_dict, template_dscp=None, success_analyze=False):
        """
        Equal to UI(20.12):
            UI: Configuration -> Templates -> Device Templates -> Create Template -> From Feature Template
        success:
            ret.status_code: 200
            ret.text: '{"templateId":"fe240d4b-db47-44d3-a7b7-6a9df9621dd1"}'
        """
        api = '/dataservice/template/device/feature/'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        payload = PAYLOAD.device_template_payload()

        payload["templateName"] = template_name
        payload["templateDescription"] = template_name if template_dscp is None else template_dscp
        payload["deviceType"] = device_type

        # update default feature template ID
        default_ft_name = PAYLOAD.c8000v_default_feature_template()
        for tp in payload["generalTemplates"]:
            tp["templateId"] = ft_id_dict[default_ft_name[tp['templateType']]]
        
        # update user-defined feature template ID, sys, vpn, intf
        for key, value in mtedge_ft_name_dict.items():
            main_template = {}
            sub_template_list = []
            if key == 'sys':
                sub_template = {}
                main_template["templateId"] = ft_id_dict[value]
                main_template["templateType"] = 'cisco_system'
                sub_template["templateId"] = ft_id_dict[default_ft_name['cisco_logging']]
                sub_template["templateType"] = "cisco_logging"
                sub_template_list.append(sub_template)
                payload["generalTemplates"].append(self._generate_subTemplates(main_template, sub_template_list))
            elif key == 'tenant':
                payload["generalTemplates"].append(
                    {
                        "templateId": ft_id_dict[value],
                        "templateType": "tenant"
                    }
                )
            else:
                main_template["templateId"] = ft_id_dict[value['vpn']]
                main_template["templateType"] = 'cisco_vpn'
                for each_intf in value['intf']:
                    sub_template = {}
                    sub_template["templateId"] = ft_id_dict[each_intf]
                    sub_template["templateType"] = "cisco_vpn_interface"
                    sub_template_list.append(sub_template)

                payload["generalTemplates"].append(self._generate_subTemplates(main_template, sub_template_list))

        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()["templateId"]]
    
    def _generate_subTemplates(self, main_template, sub_templates_list):
        '''
        This is the helper function to generate subTemplates.
        '''
        payload = PAYLOAD.template_with_subTemplate_payload()
        payload.update(
            {
                "templateId": main_template['templateId'],
                "templateType": main_template['templateType']
            }
        )
        for each_sub_tp in sub_templates_list:
            payload["subTemplates"].append(
                {
                    "templateId": each_sub_tp["templateId"],
                    "templateType": each_sub_tp["templateType"]
                }
            )
        
        return payload

