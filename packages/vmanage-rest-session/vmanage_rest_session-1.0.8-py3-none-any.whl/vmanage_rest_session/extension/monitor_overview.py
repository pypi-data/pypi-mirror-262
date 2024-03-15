class MonitorOverview():

    def monitor_overview_overview_overview_DevicesOverview(self, success_analyze=False):
        """
        No UI found in 20.11
        success:
            ret.status_code: 200
            ret.text: {u'poor': 0, u'good': 4, u'fair': 1}]
        """

        api = '/dataservice/health/devices/overview'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()]

    def monitor_overview_overview_overview_ControllersWANEdges(self, success_analyze=False):
        """
        Equal to UI(20.11):
            UI: Monitor -> Overview -> Overview -> Overview -> CONTROLLERS/WAN Edges
        success:
            ret.text: api_data/monitor_overview_overview_overview_ControllersWANEdges_GET_20.11.log
            Devices Info List: ret.json()['data']
        """

        api = '/dataservice/network/connectionssummary'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]

    def monitor_overview_overview_overview_licensing(self, success_analyze=False):
        """
        Equal to UI(20.11):
            UI: Monitor -> Overview -> Overview -> Overview -> LICENSING
        success:
            ret.status_code: 200
            ret.text: api_data/monitor_overview_overview_overview_LICENSING_GET_20.11.log
            license count info = ret.json["data"]
        """

        api = '/dataservice/msla/monitoring/licensedDeviceCount'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]

    def monitor_overview_overview_WANEdgeInventory(self, filters="", success_analyze=False):
        """
        Equal to UI(20.11):
            UI: Monitor -> Overview -> Overview -> Overview
        success:
            ret.status_code: 200
            ret.text: api_data/monitor_overview_overview_WANEdgeInventory_GET_20.11.log
            summary api info dict = ret.json["data"]
        """

        api = '/dataservice/device/vedgeinventory/summary'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]


    def monitor_overview_overview_siteBfdConnectivity(self, success_analyze=False):
        """
        Equal to UI(20.11):
            UI: Monitor -> Overview -> Overview -> Site BFD Connectivity
        success:
            ret.status_code: 200
            ret.text: api_data/monitor_overview_overview_siteBfdConnectivity_GET_20.11.log
            summary api info dict = ret.json["data"]
        """

        api = '/dataservice/device/bfd/sites/summary?isCached=true'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]
