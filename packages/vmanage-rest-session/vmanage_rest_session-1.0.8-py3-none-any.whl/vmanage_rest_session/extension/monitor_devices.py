class MonitorDevices():

    def monitor_devices_devices_devices(self, filters="", success_analyze=False):
        """
        Equal to UI(20.11):
            UI: Monitor -> Devices -> Devices -> Devices -> (Left filter select) -> (refresh button)

        api: /dataservice/health/devices?page_size=12000?filter1=filter1_value&filter2=filter2_value...
        example: https://10.75.28.103:8443/dataservice/health/devices?page_size=12000&personality=vedge&reachable=true&health=green
        filters_example: {"health": "Good", "reachable": "Up", "personality":"vSmart", "control_status":"Down" }
        success:
            ret.status_code: 200
            example_api: https://10.75.28.103:8443/dataservice/health/devices?page_size=12000
            ret.text: api_data/monitor_devices_devices_GET_20.11.log
            devices_list = ret.json()['devices'']
        """
        filter_health = {
            "Good": "health=green",
            "Fair": "health=yellow",
            "Poor": "health=red"
        }

        filter_reachable = {
            "Up": "reachable=true",
            "Down": "reachable=False",
        }

        filter_personality= {
            "vSmart": "personality=vsmart",
            "vBond": "personality=vbond",
            "vManage": "personality=vmanage",
            "Edge": "personality=edge",
        }

        filter_control_status= {
            "Up": "ontrol_status=up",
            "Partial": "ontrol_status=partial",
            "Down": "ontrol_status=down",
        }

        filter_dict = {
            "health": filter_health,
            "reachable": filter_reachable,
            "personality": filter_personality,
            "control_status": filter_control_status

        }

        if isinstance(filters, dict):
            if not filters:
                raise Exception("Empty filter dict is not allowed!")

            filter_list = []

            for filter_category, filter_item in filters.items():
                if filter_category not in filter_dict:
                    raise Exception("filter_category {} is not found in {}".format(filter_category, filter_dict.keys()))

                if filter_item not in filter_dict[filter_category]:
                    raise Exception("filter_item {} is not found in {}".format(filter_item, filter_dict[filter_category].keys()))

                filter_list.append(filter_dict[filter_category][filter_item])

            # &personality=vedge&control_status=down&reachable=false&health=red
            filters = "&" + "&".join(filter_list)

        api = '/dataservice/health/devices?page_size=12000{}'.format(filters)
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if not success_analyze:
            return ret

        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()]
