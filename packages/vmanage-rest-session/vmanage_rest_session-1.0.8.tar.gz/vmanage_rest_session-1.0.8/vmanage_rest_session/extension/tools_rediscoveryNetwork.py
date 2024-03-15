import json
class ToolsRediscoverNetwork():

    def tools_rediscoverNetwork_refresh(self, success_analyze=False):
        """
        Equal to UI(20.11):
            UI: Tools -> Rediscover Network -> (refresh button)
        success:
            ret.status_code: 200
            ret.text: api_data/tools_rediscoveryNetwork_refresh_GET.log
            ret.device_list: ret.json()['data']
        """
        api = '/dataservice/device/sync_status?groupId=all'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]

    def _tools_rediscoverNetwork_rediscover_payload(self, discover_reachable_only=False):
        payload_json = {
                "action": "rediscover",
                "devices": []
        }

        ret = self.tools_rediscoverNetwork_refresh(success_analyze=True)
        if not ret[0]:
            return ret

        for device in ret[1]:
            if discover_reachable_only:
                if device['reachability'] == 'reachable':
                    payload_json["devices"].append(
                        {
                            "deviceIP": device["deviceId"],
                            "deviceId": device["uuid"]
                        }
                    )
            else:
                payload_json["devices"].append(
                    {
                        "deviceIP": device["deviceId"],
                        "deviceId": device["uuid"]
                    }
                )

        if payload_json["devices"]:
            return [True, payload_json]
        else:
            return [False, "No Device Found!"]

    def tools_rediscoverNetwork_rediscover(self, payload_json=None, success_analyze=False):
        """
        Equal to UI(20.11):
            UI: Tools -> Rediscover Network -> <Select Devices> -> Rediscover
        Payload: api_data/tools_rediscoveryNetwork_rediscover_Payload_POST_20.11.log
        success:
            ret.status_code: 200
            ret.text: ""
        """

        if payload_json is None:
            ret = self._tools_rediscoverNetwork_rediscover_payload(discover_reachable_only=True)

            if (not ret[0]) and success_analyze:
                # If get payload failed, but with success_analyze
                return ret
            elif (not ret[0]) and (not success_analyze):
                # If get payload failed, but without success_analyze
                raise Exception("{}: GET rediscoverNetwork_rediscover_payload Failed, msg: {}".format(self.ip, ret[1]))

            payload_json = ret[1]

        api = '/dataservice/device/action/rediscover'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("POST", url, data=json.dumps(payload_json))

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret]
