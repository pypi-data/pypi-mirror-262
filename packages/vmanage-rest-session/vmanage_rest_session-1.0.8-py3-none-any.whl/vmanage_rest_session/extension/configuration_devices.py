import os
import json
from ..tools.formdata import encode_multipart

class ConfigurationDevices():

    def _configuration_devices_controllers_addController_controllers_add(self, deviceIP, personality='vsmart', username='admin', password='admin', protocol="DTLS", success_analyze=False):
        """
        This is helper function for configuration_devices_controllers_addController_vsmart_add/configuration_controller_add_vbond
        """
        api = '/dataservice/system/device'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        payload = {
            "deviceIP": deviceIP,
            "username": username,
            "password": password,
            "personality": personality,
            "generateCSR": False
        }
        if personality == "vsmart":
            payload["protocol"] = protocol
        ret = self.http_request("POST", url, data=json.dumps(payload))
        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.text]

    def configuration_devices_controllers_addController_vsmart_add(self, deviceIP, username='admin', password='admin', success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Configuration -> Devices -> Controllers -> Add Controller -> vSmart
            UI value: 
                vSmart Management IP Address: deviceIP
                Username: username
                Password: password

        success:
            ret.status_code: 200
            ret.text: '{}'
        """
        return self._configuration_devices_controllers_addController_controllers_add(deviceIP=deviceIP, personality='vsmart', username=username, password=password, success_analyze=success_analyze)

    def configuration_devices_controllers_addController_vbond_add(self, deviceIP, username='admin', password='admin', success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Configuration -> Devices -> Controllers -> Add Controller -> vBond
            UI value: 
                vBond Management IP Address: deviceIP
                Username: username
                Password: password
        success:
            ret.status_code: 200
            ret.text: '{}'
        """

        return self._configuration_devices_controllers_addController_controllers_add(deviceIP=deviceIP, personality='vbond', username=username, password=password, success_analyze=success_analyze)

    def configuration_devices_controllers_get(self, success_analyze=False):
        """
        Equal to UI(20.9):
            UI: Configuration -> Devices -> Controllers -> (refresh button)
            UI value: 
        success:
            ret.status_code: 200
            ret.text: api_data/configuration_devices_controller_get_GET_20.9.log
            controller info list: ret.json()['data']
        """
        api = '/dataservice/system/device/controllers/'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]

    def get_configuration_devices_controllers_controllerInfoDict(self):
        """
        This is helper function:

            change [controller1_info_dict, controller2_info_dict, controller3_info_dict..]
            to {
                "controller1_chassis": controller1_info_dict,
                "controller2_chassis": controller2_info_dict,
                "controller3_chassis": controller3_info_dict,
                ...
            }
        """
        ret = self.configuration_devices_controllers_get(success_analyze=True)
        if not ret[0]:
            return ret

        controller_info_list = ret[1]

        chassis_EdgeInfo_dict = {}
        for controller_info in controller_info_list:
            controller_chassis = controller_info['chasisNumber']
            chassis_EdgeInfo_dict[controller_chassis] = controller_info

        return [True, chassis_EdgeInfo_dict]        

    def getControllerAddStatus_configuration_devices_controllers_addController_controllers(self):
        """
        To check controller status after added.
        """
        ret = self.configuration_devices_controllers_get(success_analyze=True)
        if not ret[0]:
            return ret

        controller_info_list = ret[1]
        return self._check_controller_mtedge_add_status(controller_info_list)

    def getmtedgeAddStatus_configuration_devices_wanedgelist(self):
        '''
        To check mt-edge status after added.
        '''
        ret = self.configuration_devices_WANEdgeList_get(success_analyze=True)
        if not ret[0]:
            return ret

        mtedge_info_list = ret[1]
        return self._check_controller_mtedge_add_status(mtedge_info_list)

    def _check_controller_mtedge_add_status(self, device_info_list):
        """
        This is helper function of 
        getControllerAddStatus_configuration_devices_controllers_addController_controllers
        and 
        getmtedgeAddStatus_configuration_devices_wanedgelist
        """

        # common fields for both controllers and mt-edge
        pass_criteria_dict = {
            "validity": "valid",
            "deviceState": "READY",
            "configStatusMessage": "In Sync"
        }

        # controller is "certInstallStatus", mt-edge is "vedgeCertificateState"
        pass_criteria_dict2 = {
            "vedgeCertificateState": "certinstalled",
            "certInstallStatus": "Installed",
        }

        pass_criteria_field = ["system-ip", "host-name"]

        for device_info in device_info_list:
            for criteria_key, criteria_value in pass_criteria_dict.items():
                if criteria_key not in device_info.keys():
                    return [False, device_info_list]
                if criteria_value != device_info[criteria_key]:
                    return [False, device_info_list]
                for must_exist_field in pass_criteria_field:
                    if must_exist_field not in device_info.keys():
                        return [False, device_info_list]
            for criteria_key, criteria_value in pass_criteria_dict2.items():
                if criteria_key in device_info.keys() and criteria_value == device_info[criteria_key]:
                    return [True, device_info_list]

        return [False, device_info_list]

    def configuration_devices_WANEdgeList_DecommissionWANEdge(self, chasisNumber, success_analyze=False):
        """
        Equal to UI(20.11):
            UI: Configuration -> Devices -> WAN Edge List -> (speicific edge) -> Decommission WAN Edge
        success:
            ret.status_code: 200
            ret.text: {"id":"256245be-7cdd-4504-8589-a84552d59340"}
        """
        api = '/dataservice/system/device/decommission/{}'.format(chasisNumber)
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("PUT", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]

        return self.get_configuration_devices_WANEdgeList_token(chasisNumber)

    def configuration_devices_WANEdgeList_get(self, success_analyze=False):
        """
        Equal to UI(20.11):
            UI: Configuration -> Devices -> WAN Edge List -> (refresh button)
        success:
            ret.status_code: 200
            ret.text: api_data/configuration_devices_WANEdgeList_get_GET_20.11.log
            edge info list = ret.json()["data"]
        """
        api = '/dataservice/system/device/vedges'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]

    def get_configuration_devices_WANEdgeList_edgeInfoDict(self):
        """
        This is helper function:

            change [edge1_info_dict, edge2_info_dict, edge3_info_dict..]
            to {
                "edge1_chassis": edge1_info_dict,
                "edge2_chassis": edge2_info_dict,
                "edge3_chassis": edge3_info_dict,
                ...
            }
        """
        ret = self.configuration_devices_WANEdgeList_get(success_analyze=True)
        if not ret[0]:
            return ret

        edges_info_list = ret[1]

        chassis_EdgeInfo_dict = {}
        for edge_info in edges_info_list:
            edge_chassis = edge_info['chasisNumber']
            chassis_EdgeInfo_dict[edge_chassis] = edge_info

        return [True, chassis_EdgeInfo_dict]

    def check_configuration_devices_WANEdgeList_validity(self, chasisNumber, chassis_EdgeInfo_dict=None):
        """
        This is helper function to check speicific chassis_number validity in UI
        UI(20.11): Configuration -> Devices -> WAN Edge List -> (speicific edge) -> Validity
        """
        if not chassis_EdgeInfo_dict:
            ret = self.get_configuration_devices_WANEdgeList_edgeInfoDict()
            if not ret[0]:
                return ret

            chassis_EdgeInfo_dict = ret[1]

        if chasisNumber not in chassis_EdgeInfo_dict:
            return [False, "{} does not exist, skip".format(chasisNumber)]

        if 'validity' not in chassis_EdgeInfo_dict[chasisNumber]:
            return [False, "validity is not in {}".format(chassis_EdgeInfo_dict[chasisNumber])]

        if chassis_EdgeInfo_dict[chasisNumber]['validity'] != 'valid':
            return [False, chassis_EdgeInfo_dict[chasisNumber]['validity']]
        else:
            return [True, "valid"]

    def get_configuration_devices_WANEdgeList_token(self, chasisNumber):
        """
        This is helper function to get speicific chassis_number token
        UI(20.11): Configuration -> Devices -> WAN Edge List -> (speicific edge) -> Serial No./Token
        """
        ret = self.get_configuration_devices_WANEdgeList_edgeInfoDict()
        if not ret[0]:
            return ret

        chassis_EdgeInfo_dict = ret[1]
        if chasisNumber not in chassis_EdgeInfo_dict:
            return [False, "{} is not found in {}".format(chasisNumber, chassis_EdgeInfo_dict.keys())]

        if chassis_EdgeInfo_dict[chasisNumber]['vedgeCertificateState'] != "tokengenerated":
            return [False, chassis_EdgeInfo_dict[chasisNumber]['vedgeCertificateState']]

        token = chassis_EdgeInfo_dict[chasisNumber]['serialNumber']
        return [True, token]

    def configuration_devices_WANEdgeList_DeleteWANEdge(self, chasisNumber, success_analyze=False):
        """
        Equal to UI(20.11):
            UI: Configuration -> Devices -> WAN Edge List -> (speicific edge) -> Delete WAN Edge
        success:
            ret.status_code: 200
            ret.text: {"status":"success"}
        """
        api = '/dataservice/system/device/{}'.format(chasisNumber)
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("DELETE", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret]

    def robust_configuration_devices_WANEdgeList_DeleteWANEdge(self, chasisNumber, serialNumber=None, check_chassis_exists=True, invalid_if_needed=True):
        """
        This is helper function for configuration_devices_WANEdgeList_DeleteWANEdge
        It add chassisNumber validity check, certerticate sync status check, invalid devices if it is not
        """
        if check_chassis_exists:
            ret = self.get_configuration_devices_WANEdgeList_edgeInfoDict()
            if not ret[0]:
                return ret

            chassis_EdgeInfo_dict = ret[1]
            if chasisNumber not in chassis_EdgeInfo_dict:
                return [False, "{} does not exist, skip".format(chasisNumber)]

        if invalid_if_needed:
            ret = self.check_configuration_devices_WANEdgeList_validity(chasisNumber)
            if ret[0]:
                valid_ret = self.waitUntilSynced_configuration_certificates_WANEdgeList_InvalidValid(chasisNumber, serialNumber=serialNumber, send_to_controller=True)
                if not valid_ret[0]:
                    return valid_ret

        return self.configuration_devices_WANEdgeList_DeleteWANEdge(chasisNumber)

    def batchDelete_configuration_devices_WANEdgeList_DeleteWANEdge(self, delete_edge_info=None, check_chassis_exists=True, invalid_if_needed=True):
        """
        This is helper function for configuration_devices_WANEdgeList_DeleteWANEdge
        It will delete massive devices in one time
        delete_edge_info:
            if it is None, it will delete all the edge devices
            if it is list, it should be chassis list, [chassis1, chassis2 ...]
            if it is dict, it should be {chassis1: serial1, chassis2: serial2...}
        """
        ret = self.checkSyncd_configuration_certificates_WANEdgeList_SendToControllers_status()
        if not ret[0]:
            # Send to Controllers is Red, needs to sync the status to the controllers
            ret = self.push_configuration_certificates_WANEdgeList_SendToControllers()
            if not ret[0]:
                return ret

        if delete_edge_info is None:
            # If delete_edge_info not provide, Get All Edge devices Info Dict, delete all edges
            ret = self.get_configuration_devices_WANEdgeList_edgeInfoDict()
            if not ret[0]:
                return ret

            chassis_EdgeInfo_dict = ret[1]

            delete_edge_info = {}
            for edge_chassis, chassis_EdgeInfo in chassis_EdgeInfo_dict.items():
                delete_edge_info[edge_chassis] = chassis_EdgeInfo["serialNumber"]

            check_chassis_exists = False
        elif isinstance(delete_edge_info, list):
            # Change list to dict, key is the chassis, value is the serial
            ret = self.get_configuration_devices_WANEdgeList_edgeInfoDict()
            if not ret[0]:
                return ret
            chassis_EdgeInfo_dict = ret[1]

            _delete_edge_info = {}
            for edge_chassis in delete_edge_info:
                if edge_chassis not in chassis_EdgeInfo_dict:
                    print("{} does not exists, skip the delete".format(edge_chassis))
                    continue

                _delete_edge_info[edge_chassis] = chassis_EdgeInfo_dict[edge_chassis]["serialNumber"]

            delete_edge_info = _delete_edge_info
            check_chassis_exists = False

        if check_chassis_exists:
            ret = self.get_configuration_devices_WANEdgeList_edgeInfoDict()
            if not ret[0]:
                return ret

            chassis_EdgeInfo_dict = ret[1]

        # Invalid all the devices, suppose all the devices are valid, all it might have a failure
        for chasisNumber, serialNumber in delete_edge_info.items():
            print("Invalid Edge device: {}, serial number: {}".format(chasisNumber, serialNumber))
            valid_ret = self.configuration_certificates_WANEdgeList_InvalidValid(chasisNumber=chasisNumber, serialNumber=serialNumber, valid=False, success_analyze=True)
            if not valid_ret[0]:
                return valid_ret

        print("Send Edge list information to Controllers")
        ret = self.push_configuration_certificates_WANEdgeList_SendToControllers()
        if not ret[0]:
            return ret

        # At last delete all the devices
        for chasisNumber in delete_edge_info:
            print("Delete Edge: {}".format(chasisNumber))
            ret = self.configuration_devices_WANEdgeList_DeleteWANEdge(chasisNumber, success_analyze=True)
            if not ret[0]:
                return ret

        return [True, "{} got deleted".format(delete_edge_info.keys())]

    def configuration_devices_WANEdgeList_UploadWANEdgeList(self, viptela_serial_file, file_name=None, valid=True, success_analyze=False):
        """
        Equal to UI(20.11):
            UI: Configuration -> Devices -> WAN Edge List -> Upload WAN Edge List -> Upload WAN Edge List
        Payload Detail: api_data/configuration_devices_WANEdgeList_UploadWANEdgeList_Payload_POST_20.11.log
        success:
            ret.status_code: 200
            ret.text: api_data/configuration_devices_WANEdgeList_UploadWANEdgeList_POST_20.11.log
        """
        # if viptela_serial_file is a file name, open the file and get the content
        if isinstance(viptela_serial_file, str) and os.path.isfile(viptela_serial_file):
            with open(viptela_serial_file, 'rb') as f:
                viptela_serial_file = f.read()

        json_data = {
            'validity': "valid" if valid else "invalid",
            "upload": True
        }
        fields = {'data': json.dumps(json_data)}
        files = {
                 'file':
                     {
                        'filename': file_name if file_name is not None else "serial.viptela",
                        'content': viptela_serial_file,
                        'mimetype': 'multipart/form-data'
                      }
                }
        payload, headers = encode_multipart(fields, files)
        for key, value in self.secHeaders.items():
            if key not in headers:
                headers[key] = self.secHeaders[key]

        api = '/dataservice/system/device/fileupload'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("POST", url, headers=headers, data=payload)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()]
