class Extension(object):

    def get_device_inventory_summary(self):
        url = 'https://{}:{}/dataservice/device/vedgeinventory/summary' \
              .format(self.ip, self.port)
        api_ret = self.http_request("GET", url)

        if api_ret.status_code != 200:
            return [False, api_ret]
        else:
            edges_data = api_ret.json()['data']
            
            return [True, edges_data]
