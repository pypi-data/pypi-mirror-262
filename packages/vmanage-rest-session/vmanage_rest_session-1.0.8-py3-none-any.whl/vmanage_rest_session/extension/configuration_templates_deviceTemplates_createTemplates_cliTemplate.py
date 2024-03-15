import json
import time
from ..tools.cli_template_utils import filter_cli_config

class ConfigurationTemplatesCliTemplate():

    def configuration_templates_deviceTemplates_cliTemplate_deviceModule(self, device_module="vsmart", success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Configuration -> Templates -> Device Templates -> Create Template -> Cli Template -> Device Module -> (select specific device-module)
        success:
            ret.status_code: 200
            ret.text: api_data/configuration_templates_deviceTemplates_cliTemplate_deviceModule_GET_20.9.log
            return currently connected available device list = ret.json()["data"]
        Usage: To get the available device
        """

        api = "/dataservice/device?device-model={}&reachability=reachable".format(device_module)
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]

    def configuration_templates_deviceTemplates_cliTemplate_LoadRunningConfigFromDevice(self, device_uuid, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Configuration -> Templates -> Device Templates -> Create Template -> Cli Template -> Load Running config from reachable device -> (select specific device)
        success:
            ret.status_code: 200
            ret.text: api_data/configuration_templates_deviceTemplates_cliTemplate_LoadRunningConfigFromDevice_GET_20.9.log
            device cli configure = ret.json()["config"]
        """
        api = "/dataservice/template/config/running/{}".format(device_uuid)
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()["config"]]

    def configuration_templates_deviceTemplates_cliTemplate_addCliTemplate(self, template_name, device_type, template_config, template_discription=None, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Configuration -> Templates -> Device Templates -> Create Template -> Cli Template -> (Create Template...)
        success:
            ret.status_code: 200
            ret.text: ret.text = '{"templateId":"bfabcbeb-7000-467e-afd0-6b8a589663b2"}'
        """
        api = "/dataservice/template/device/cli"
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        payload = {
            "templateName": template_name,
            "templateDescription": template_name if template_discription is None else template_discription,
            "deviceType": device_type,
            "templateConfiguration": filter_cli_config(template_config),
            "factoryDefault": False,
            "configType": "file"
        }
        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()]

    def configuration_templates_deviceTemplates_cliTemplate_deleteTemplate(self, template_id, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Configuration -> Templates -> Device Templates -> Create Template -> (specific template) -> Delete
        success:
            ret.status_code: 200
            ret.text: ""
        """
        api = "/dataservice/template/device/{}".format(template_id)
        url = 'https://{}:{}{}'.format(rest_session.ip, rest_session.port, api)
        ret = rest_session.http_request("DELETE", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret]

    def configuration_templates_deviceTemplates_statusGet(self, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Configuration -> Templates -> Device Templates -> (Refresh button get_template status...)
        success:
            ret.status_code: 200
            ret.text: api_data/configuration_templates_deviceTemplates_statusGet_GET_20.9.log
            success: ret.json()["data"] = []
        """

        api = "/dataservice/template/device/syncstatus/"
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        
        if ret.json()['data']:
            return [False, ret.json()['data']]
        else:
            return [True, ret.json()['data']]

    def configuration_templates_deviceTemplates_getTemplate(self, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Configuration -> Templates -> Device Templates -> (Refresh button get_template list...)
        success:
            ret.status_code: 200
            ret.text: api_data/configuration_templates_deviceTemplates_getTemplate_GET_20.9.log
            template list: ret.json()["data"]
        """

        api = "/dataservice/template/device"
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]

    def getTemplateID_configuration_templates_deviceTemplates_getTemplate(self, template_name):
        """
        Here is the helper function to get the device templateId from template_name
        """

        ret = self.configuration_templates_deviceTemplates_getTemplate(success_analyze=True)
        if not ret[0]:
            return ret

        template_list = ret[1]

        for template in template_list:
            if template_name == template["templateName"]:
                return [True, template]

        return [False, template_list]

    def configuration_templates_deviceTemplates_attachDevices(self, template_id, devices, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Configuration -> Templates -> Device Templates -> (specific template) -> Attach Devices
        success:
            ret.status_code: 200
            devices is device csv list, Example:
                [
                    {
                        "csv-status": "complete",
                        "csv-deviceId": "d6e188ae-ae40-446d-bd32-1f34156de644",
                        "csv-deviceIP": "172.16.255.20",
                        "csv-host-name": "vm10",
                        "csv-templateId": "2f37c454-fb3d-4978-9154-8fabcf1c085f"
                    },
                    {
                        "csv-status": "complete",
                        "csv-deviceId": "314f8c48-a510-4b0b-8e43-71c66e5b3f68",
                        "csv-deviceIP": "172.16.255.19",
                        "csv-host-name": "vm9",
                        "csv-templateId": "2f37c454-fb3d-4978-9154-8fabcf1c085f"
                    }
                ]
            ret.text: {"id":"push_file_template_configuration-b3b6dfec-2b82-4d2b-b573-f4ad875da09c"}
        payload: api_data/configuration_templates_deviceTemplates_attachDevices_Payload_POST_20.9.log
        """
        api = "/dataservice/template/device/config/attachcli"
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        payload = {
            "deviceTemplateList":
            [
                {
                    "templateId": template_id,
                    "device": devices,
                    "isEdited": False
                }
            ]
        }
        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()]

    def configuration_templates_deviceTemplates_attachDevices_getDeviceCsv(self, template_id, device_uuid, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Configuration -> Templates -> Device Templates -> (specific template) -> Attach Devices -> (Before Template Push, vManage will get Device CSV)
        success:
            ret.status_code: 200
            payload: 
                {
                    "templateId": "14c68be2-18be-440a-8591-2b396e48154d",
                    "deviceIds":
                    [
                        "0d485701-2d9c-4f91-88e2-f9212484c0d8"
                    ],
                    "isEdited": false,
                    "isMasterEdited": false
                }
            ret.text: api_data/configuration_templates_deviceTemplates_attachDevices_getDeviceCsv_POST_20.9.log
            ret.json()['data']:
                    [
                        {
                            "csv-status": "complete",
                            "csv-deviceId": "0d485701-2d9c-4f91-88e2-f9212484c0d8",
                            "csv-deviceIP": "1.1.1.11",
                            "csv-host-name": "MT1_vsmart1"
                        }
                    ]
        """
        api = "/dataservice/template/device/config/input/"
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        payload = {
                    "templateId": template_id,
                    "deviceIds":
                    [
                        device_uuid
                    ],
                    "isEdited": False,
                    "isMasterEdited": False,
                }
        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            device_list = ret.json()['data']
            for device in device_list:
                device["csv-templateId"] = template_id
            return [True, device_list]  

    def attache1DeviceAPI_configuration_templates_deviceTemplates_attachDevices(self, template_id, device_uuid, default_mode='cli', device_csv=None):
        """
        This is helper function for configuration_templates_deviceTemplates_attachDevices_getDeviceCsv and configuration_templates_deviceTemplates_attachDevices
        """
        ret = self.configuration_templates_deviceTemplates_attachDevices_getDeviceCsv(template_id, device_uuid, success_analyze=True)
        if not ret[0]:
            return ret

        if default_mode == 'cli':
            return self.configuration_templates_deviceTemplates_attachDevices(template_id, ret[1], success_analyze=True)
        else:
            if ret[1][0]['csv-status'] == 'in_complete':
                tmp_sysip = ret[1][0]['csv-deviceIP']
                ret[1][0]['csv-status'] = 'complete'
                ret[1][0]['//system/host-name'] = device_csv['host-name']
                ret[1][0]['csv-deviceIP'] = device_csv['deviceIP']
                ret[1][0]['//system/system-ip'] = tmp_sysip
                ret[1][0].update({'csv-templateId': template_id})

            return self.configuration_templates_deviceTemplates_attachDevices_deviceTemplate(template_id, ret[1], success_analyze=True)

    def attache1DeviceManual_configuration_templates_deviceTemplates_attachDevices(self, template_id, device_uuid, device_ip, device_hostname, success_analyze=False):
        """
        This is helper function for configuration_templates_deviceTemplates_attachDevices to attach 1 device
        """
        devices = [
                {
                    "csv-status": "complete",
                    "csv-deviceId": device_uuid,
                    "csv-deviceIP": device_ip,
                    "csv-host-name": device_hostname,
                    "csv-templateId": template_id,
                }
            ]
        return self.configuration_templates_deviceTemplates_attachDevices(template_id=template_id, devices=devices, success_analyze=success_analyze)

    def configuration_templates_deviceTemplates_detachDevices(self, device_uuid, device_ip, device_type, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Configuration -> Templates -> Device Templates -> (specific template) -> Detach Devices
        success:
            ret.status_code: 200
            ret.text: {"id":"device_config_mode_cli-1a24dac4-4e09-4441-81e5-fbae5682b594"}
        payload: {"deviceType":"controller","devices":[{"deviceId":"bede074f-96ab-4b3e-b350-f0a94d86af1d","deviceIP":"169.254.10.4"}]}
        """

        api = "/dataservice/template/config/device/mode/cli"
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        payload = {
            "deviceType": device_type,
            "devices": [
                    {
                        "deviceId": device_uuid,
                        "deviceIP": device_ip
                    }
                ]
        }
        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()]

    def get_push_status(self, push_id, success_analyze=False):
        """
        This is just same function as getPushStatus_configuration_templates_deviceTemplates_attachDetachDevices
        """
        return self.getPushStatus_configuration_templates_deviceTemplates_attachDetachDevices(push_id, success_analyze)

    def getPushStatus_configuration_templates_deviceTemplates_attachDetachDevices(self, push_id, success_analyze=False):
        """
        There is the API to check the template push status, it also used to track others push status such as tenant push
        success:
            ret.status_code: 200
            ret.text: api_data/getTemplateAttachStatus_configuration_templates_deviceTemplates_attachDevices_GET_20.9.log
            success attached: ret.josn()['summary']['count']['success'] == x
            failed attached: ret.josn()['summary']['count']['Failure'] == y
        """

        api = "/dataservice/device/action/status/{}".format(push_id)
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()]

    def wait_push_result(self, push_id, maxi_wait=360):
        """
        This is the same function as the waitPushResult_configuration_templates_deviceTemplates_attachDetachDevices
        """
        return self.waitPushResult_configuration_templates_deviceTemplates_attachDetachDevices(push_id, maxi_wait)

    def waitPushResult_configuration_templates_deviceTemplates_attachDetachDevices(self, push_id, maxi_wait=360):
        """
        This is helper function to wait for getPushStatus_configuration_templates_deviceTemplates_attachDetachDevices finished.
        ret.josn()['summary']["status"] = done
        success:
            no "Failure" in attached: ret.josn()['summary']['count']
                ret.josn()['summary']['count']['Failure'] == y
        """
        start_timer = time.time()

        while True:
            ret = self.getPushStatus_configuration_templates_deviceTemplates_attachDetachDevices(push_id, success_analyze=True)
            if not ret[0]:
                return ret

            if time.time() - start_timer > maxi_wait:
                break

            if ret[1]['summary']["status"] == "done":
                break

        if 'Failure' in ret[1]['summary']['count']:
            return [False, ret[1]]

        return [True, ret[1]]

    def configuration_templates_deviceTemplates_attachDevices_deviceTemplate(self, template_id, devices, success_analyze=False):
        """
        Equal to UI(20.12):
            UI: Configuration -> Templates -> Device Templates -> (specific device template) -> Attach Devices
        success:
            ret.status_code: 200
            devices is device csv list, Example:
                [
                    {
                        "csv-status": "complete",
                        "csv-deviceId": "C8K-eb3b3528-847f-4f2a-8a31-e08df62e9494",
                        "csv-deviceIP": "169.254.10.23",
                        "csv-host-name": "mtedge1",
                        "//system/host-name": "mtedge1",
                        "//system/system-ip": "172.16.254.215",
                        "csv-templateId": "46955e91-eb02-447d-9985-67a830bac9af"
                    }
                ]
            ret.text: {"id":"push_file_template_configuration-b3b6dfec-2b82-4d2b-b573-f4ad875da09c"}
        payload: api_data/configuration_templates_deviceTemplates_attachDevices_devTP_Payload_POST_20.12.log
        """
        api = "/dataservice/template/device/config/attachfeature"
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        payload = {
            "deviceTemplateList":
            [
                {
                    "templateId": template_id,
                    "device": devices,
                    "isEdited": False,
                    "isMasterEdited": False
                }
            ]
        }
        
        ret = self.http_request("POST", url, data=json.dumps(payload))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()]

