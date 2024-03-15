# vManage REST Session
vmanage rest api session

# Support Platform
Win/Mac/Linux

# 1. How-To Quick-Start

```bash

# pip Installation
demon@scale-jumpServer01:~$ python -m pip install git+https://sdwan-git.cisco.com/crdc-tools/vmanage_rest_session

# Quick Start
demon@scale-jumpServer01:~$ python
>>> from vmanage_rest_session.vmanage_session import VmanageAPI
>>> rs = VmanageAPI(ip="10.75.212.20", username="admin", password="Login_999", port=8443)
>>> ret = rs.get_configuration_devices_controllers_controllerInfoDict()
>>> ret[0], ret[1].keys()
(True, dict_keys(['2b6f5dca-6d1a-4e85-b1ca-e1609e0e1ca2', 'c2844354-741e-4d2f-b586-f193d1456416', '8ad56298-6f7a-42a4-8182-d34a2160a5dd']))
>>> ret[1]['2b6f5dca-6d1a-4e85-b1ca-e1609e0e1ca2']['host-name']
'vmanage'
>>>

```


## 2. Get Method Help

### 2.1 Get all available methods
<details><summary>rs.list_all_methods()</summary>
<p>


```bash

# 1. List all methods
>>> rs.list_all_methods()
All available methods:
...
  configuration_devices_WANEdgeList_UploadWANEdgeList
  configuration_devices_WANEdgeList_get
  configuration_devices_controllers_addController_vbond_add
  configuration_devices_controllers_addController_vsmart_add
  configuration_devices_controllers_get
  configuration_templates_deviceTemplates_attachDevices
  configuration_templates_deviceTemplates_attachDevices_getDeviceCsv
  configuration_templates_deviceTemplates_cliTemplate_LoadRunningConfigFromDevice
  configuration_templates_deviceTemplates_cliTemplate_addCliTemplate
  configuration_templates_deviceTemplates_cliTemplate_deleteTemplate
  configuration_templates_deviceTemplates_cliTemplate_deviceModule
  configuration_templates_deviceTemplates_detachDevices
  configuration_templates_deviceTemplates_getTemplate
  configuration_templates_deviceTemplates_statusGet
...
# 2. Filter with Keywords
>>> rs.list_all_methods("configuration_devices_controllers")
All available methods with keyword: 'configuration_devices_controllers'
  _configuration_devices_controllers_addController_controllers_add
  configuration_devices_controllers_addController_vbond_add
  configuration_devices_controllers_addController_vsmart_add
  configuration_devices_controllers_get
  getControllerAddStatus_configuration_devices_controllers_addController_controllers
>>>
# 3. Filter with Regular Express
>>> rs.list_all_methods("^configuration_devices_controllers", regrex=True)
All available methods with keyword: '^configuration_devices_controllers'
  configuration_devices_controllers_addController_vbond_add
  configuration_devices_controllers_addController_vsmart_add
  configuration_devices_controllers_get
>>>

```

</details>


### 2.2 Get method help

<details><summary>help(rs.method_name)</summary>
<p>

```bash

>>> help(rs.configuration_devices_controllers_get)

configuration_devices_controllers_get(success_analyze=False) method of vmanage_rest_session.vmanage_session.VmanageAPI instance
    Equal to UI(20.9):
        UI: Configuration -> Devices -> Controllers -> (refresh button)
        UI value:
    success:
        ret.status_code: 200
        ret.text: api_data/configuration_devices_controller_get_GET_20.9.log
        controller info list: ret.json()['data']
(END)

```
</details>


### 2.2 Get method definition file

<details><summary>rs.get_file(method_name)</summary>
<p>

```bash

>>> rs.get_file("configuration_devices_controllers_get")
Definition File: /usr/local/lib/python3.7/site-packages/vmanage_rest_session/extension/configuration_devices.py
>>>
```
</details>


### 2.3 Get method related API response file

<details><summary>rs.get_log(method_name)</summary>
<p>

```bash

>>> rs.get_log("configuration_devices_controller")
Totally found 1 files:
  configuration_devices_controller_get_GET_20.9.log
>>>
>>> rs.show_log("configuration_devices_controller_get_GET_20.9.log")
...
"data":
    [
        {
            "deviceType": "vbond",
            "serialNumber": "303C86B3B82A8EAD",
            "ncsDeviceName": "vbond-92f9232c-6eb7-4fe6-8248-c312ecce0407",
            "configStatusMessage": "In Sync",
            "templateApplyLog":
            [
                "[16-Apr-2023 10:53:11 UTC] Sync-from successful"
            ],
            "uuid": "92f9232c-6eb7-4fe6-8248-c312ecce0407",
            "managementSystemIP": "169.254.10.2",
            "templateStatus": "Success",
            "chasisNumber": "92f9232c-6eb7-4fe6-8248-c312ecce0407",
            "configStatusMessageDetails": "",
            "configOperationMode": "cli",
            "deviceModel": "vedge-cloud",
...
    ]
>>>

```
</details>


## 3. Create and Load Your Own Extension
  3.1 module name must be named as `vmanage_<your_extension_module_name>.py` \
  3.2 class name must be named as `class Extension(object):` \
  3.3 Load your extension should be  `rs.load_extension("your_extension_module_name", module_path=your_module_path)` \
  3.4 when you call your method, call it as `rs.<your_extension_module_name>_<your_method_name>`

```python

# 1. Create a extension file called "myextension"
demon@scale-jumpServer01:~/rs_script$ cat > vmanage_myextension.py
class Extension(object):
    def get_device_inventory_summary(self, success_analyze=False):
        api = '/dataservice/device/vedgeinventory/summary'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)
        if not success_analyze:
            return ret
        if ret.status_code != 200:
            return [False, ret]
        else:
            return [True, ret.json()['data']]
demon@scale-jumpServer01:~/rs_script$ python
>>> from vmanage_rest_session.vmanage_session import VmanageAPI
>>> rs = VmanageAPI(ip="10.75.212.20", username="admin", password="Login_999", port=8443)

# 2. Load "myextension" extension
>>> rs.load_extension("myextension", module_path="/home/demon/rs_script")

# 3. List "myextension" defined methods
>>> rs.list_all_methods("myextension")
All available methods with keyword: 'myextension'
  myextension_get_device_inventory_summary

# 4. Load "myextension" extension specific method
>>> ret = rs.myextension_get_device_inventory_summary(success_analyze=True)
```

## 4. MultiTenant Related
<details><summary>MT Related Operation</summary>
<p>


```bash

# 1. Login with tenant name

>>> from vmanage_rest_session.vmanage_session import VmanageAPI
>>> orange_inc = VmanageAPI("10.75.221.236", port=10100, is_mtt=True, org_name='vIPtela Inc Regression-Orange Inc')
>>> apple_inc = VmanageAPI("10.75.221.236", port=10100, is_mtt=True, org_name='vIPtela Inc Regression-Apple Inc')


# 2. Login the admin tenant, jump to sepcific tenant

>>> from vmanage_rest_session.vmanage_session import VmanageAPI
>>> rs = VmanageAPI("10.75.221.236", port=10100)
>>> rs.is_mtt = True
>>> rs.relogin('vIPtela Inc Regression-Orange Inc')

```
</details>

