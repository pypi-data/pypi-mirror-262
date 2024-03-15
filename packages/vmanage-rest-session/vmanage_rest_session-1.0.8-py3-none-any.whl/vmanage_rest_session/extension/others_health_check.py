class HealthCheck():

    def server_ready(self, success_analyze=True):
        """
            server_ready is the same function with health_check_server_ready
            since server_ready is a common name, so we add it for compatibility
            And it does not follow the common name rule
        """
        return self.health_check_server_ready(success_analyze)

    def health_check_server_ready(self, success_analyze=False):
        """
        not_ready(application-server restart):
            ret.status_code: 503
            ret.text: confused office man page we always met...
        ready: 
            ret.status_code: 200
            ret.text: {"isServerReady":true}
        """
        api = '/dataservice/client/server/ready'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()]
