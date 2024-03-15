import time

class ConfigurationCertificates():

    def configuration_certificates_controllers_get(self, success_analyze=False):
        """
        UI(20.9):
            UI: configuration -> Certificates -> Controllers -> (refresh button)
            UI value:
                Organization: org_name
        success:
            ret.status_code: 200
            ret.text: api_data/configuration_certificates_controllers_GET_2.11.log
                controller_list_info = ret.json()["data"]
        """
        api = '/dataservice/certificate/record'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]

    def configuration_certificates_WANEdgeList_SendToControllers(self, success_analyze=False):
        """
        UI(20.11):
            UI: configuration -> Certificates -> WAN Edge List -> Send to Controllers
        success:
            ret.status_code: 200
            ret.text: {"id":"eeee84eb-cb48-4866-b239-4bd4ce486923"}
        """
        # api = '/dataservice/certificate/vedge/list?action=push'
        api = '/dataservice/certificate/vedge/list'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("POST", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.text]

    def push_configuration_certificates_WANEdgeList_SendToControllers(self, max_wait=360):
        """
        This is helper function to send configuration_certificates_WANEdgeList_SendToControllers
        Also it can check configuration_certificates_WANEdgeList_SendToControllers_status to be synced
        """
        ret = self.configuration_certificates_WANEdgeList_SendToControllers(success_analyze=True)
        if not ret[0]:
            return ret

        return self.waitUntil_configuration_certificates_WANEdgeList_SendToControllers_synced(max_wait)

    def configuration_certificates_WANEdgeList_SendToControllers_status(self, success_analyze=True):
        """
        UI(20.11):
            UI: configuration -> Certificates -> WAN Edge List -> Send to Controllers
            After push the vEdge list, there is the push status page, here is the api to check the status
        success:
            ret.status_code: 200
            ret.text: api_data/configuration_certificates_WANEdgeList_SendToControllers_status_GET_20.11.log
            ret.json()['data] =[
                                {
                                    "totalControllers": 4,
                                    "ControllersOutOfSync": 0,
                                    "tenantList":
                                    []
                                }
                            ]
        """
        api = '/dataservice/system/device/controllers/vedge/status'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]

    def waitUntil_configuration_certificates_WANEdgeList_SendToControllers_synced(self, max_wait=360):
        """
        This is helper function check configuration_certificates_WANEdgeList_SendToControllers_status synced
        """
        start_time = time.time()

        while True:
            ret = self.configuration_certificates_WANEdgeList_SendToControllers_status(success_analyze=True)
            if not ret[0]:
                return ret

            out_sync_edge_num = ret[1][0]['ControllersOutOfSync']
            if int(out_sync_edge_num) == 0:
                return [True, "All synced"]

            if time.time() - start_time > max_wait:
                err_msg = "Wait for around {}s, still not sync, skip".format(max_wait)
                return [False, err_msg]

    def checkSyncd_configuration_certificates_WANEdgeList_SendToControllers_status(self):
        """
        Same API with configuration_certificates_WANEdgeList_SendToControllers_status
        But here we are checking the button of "Send to Controllers" is read or not
        """
        ret = self.configuration_certificates_WANEdgeList_SendToControllers_status(success_analyze=True)

        if not ret[0]:
            return ret

        out_sync_edge_num = ret[1][0]['ControllersOutOfSync']

        if int(out_sync_edge_num) == 0:
            return [True, "All synced"]
        else:
            return [False, ret[1]]

    def configuration_certificates_WANEdgeList_InvalidValid(self, chasisNumber, serialNumber, valid=False, success_analyze=False):
        """
        Equal to UI(20.11):
            UI: Configuration -> certificates -> WAN Edge List -> Validity(valid/invalid)
        payload: [{"chasisNumber":"89cdefff-51f8-4e54-8df0-ded2e3eefb41","serialNumber":"AC61D3868E3E2A82","validity":"invalid"}]
        success:
            ret.status_code: 200
            ret.text: {"id":"4323287c-1594-457c-8cbd-1aaac99db2fc"}
        """

        api = '/dataservice/certificate/save/vedge/list'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)

        if valid:
            payload = '[{"chasisNumber":"' + str(chasisNumber) \
                      + '","serialNumber":"' + str(serialNumber) \
                      + '","validity":"valid"}]'
        else:
            payload = '[{"chasisNumber":"' + str(chasisNumber) \
                      + '","serialNumber":"' + str(serialNumber) \
                      + '","validity":"invalid"}]'

        ret = self.http_request("POST", url, data=payload)

        if not success_analyze:
            return ret

        # Here we have a issue, actually the ret status code 200 only shows the API has sccessully sent, doesn't mean it is successfully done
        if ret.status_code != 200:
            return [False, ret.text]
        else:
            return [True, ret.text]

    def waitUntilSynced_configuration_certificates_WANEdgeList_InvalidValid(self, chasisNumber, serialNumber=None, valid=False, send_to_controller=True):
        """
        This is helper function to invalid/valid a specific devices based on the chassisNumber using configuration_certificates_WANEdgeList_InvalidValid
        and it also can send to Controllers the information and wait for status syncd
        """
        if serialNumber is None:
            ret = self.get_configuration_devices_WANEdgeList_edgeInfoDict()
            if not ret[0]:
                return ret
            chassis_EdgeInfo_dict = ret[1]

            if chasisNumber not in chassis_EdgeInfo_dict:
                return [False, "{} does not exist, skip".format(chasisNumber)]

            serialNumber = chassis_EdgeInfo_dict[chasisNumber]['serialNumber']

        ret = self.configuration_certificates_WANEdgeList_InvalidValid(chasisNumber, serialNumber, valid, success_analyze=True)

        if not ret[0]:
            return ret

        if send_to_controller:
            return self.push_configuration_certificates_WANEdgeList_SendToControllers()

        return [True, "Successfully invalid it"]

