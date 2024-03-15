class VmanageInternal():

    def vmanage_internal_notification_queueInfo_get(self, success_analyze=False):
        """
        success:
            ret.status_code: 200
            ret.text: {u'syncing': [], u'Stuck': {}, u'queued': []}]
        """
        api = '/dataservice/device/queues'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()]

    def vmanage_internal_system_device_sync_rootcertchain(self, success_analyze=False):
        """
        success:
            ret.status_code: 200
            ret.text: {"syncRootCertChain":"done"}
        """
        api = '/dataservice/system/device/sync/rootcertchain'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()]

    def vmanage_internal_stats_collect(self, success_analyze=False):
        """
        success:
            ret.status_code: 200
            ret.text: {"ActivateDataCollection":"success"}
        """
        api = '/dataservice/statistics/collect'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.text]

    def vmanage_internal_stats_process(self, success_analyze=False):
        """
        success:
            ret.status_code: 200
            ret.text: {"ActivateDataProcessing":"success"}
        """
        api = '/dataservice/statistics/process'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.text]
