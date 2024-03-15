import os
import re
import sys
import glob
import time
import copy
import json
import types
import inspect
import warnings
warnings.filterwarnings(action='ignore', module='.*OpenSSL.*')
import requests  # noqa: E402
from requests.packages.urllib3.exceptions import \
    InsecureRequestWarning  # noqa: E402
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


from .internal_extension import module_class_list

PY2 = sys.version_info.major == 2

if PY2:
    import imp
    from .tools.toolspy2 import tcp_port_alive
else:
    from .tools.tools import tcp_port_alive
    import importlib.util

class VmanageAPI(object):

    def __init__(
        self,
        ip,
        username="admin",
        password="Cisco#123@Viptela",
        port=8443,
        **kwargs
    ):
        self.secHeaders = {}
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.org_name = None
        self.is_mtt = False
        self.kwargs =kwargs

        self.approximate_match = False

        for attribute in kwargs:
            setattr(self, attribute, kwargs[attribute])

        self.login()

        # Todolist: dynamic load using class or instance
        # Load Extension Module, later will support dynamic user-defined load support
        self.module_class_list = self.module_filter(module_class_list)
        if self.module_class_list:
            self._load_modules(self.module_class_list)

    def __getattr__(self, attr):
        # dir will call __getattr__ to get all attributes, so please do not use it
        if self.approximate_match:
            for _attr in vars(self):
                if "__" in attr:
                    continue
                if attr in _attr:
                    ins = getattr(self, _attr)
                    if isinstance(ins, types.MethodType):
                        return ins
        raise AttributeError("Attribute: {} is not found".format(attr))

    def _load_modules(self, module_class_list):
        for cls in module_class_list:
            for _attr in dir(cls):
                if "__" in _attr:
                    continue
                function = getattr(cls, _attr)
                if PY2:
                    try:
                        function = function.__func__
                    except:
                        pass

                if isinstance(function, types.FunctionType):
                    bound_method = function.__get__(self, self.__class__)
                    setattr(self, function.__name__, bound_method)

    def module_filter(self, module_class_list):
        user_selected_module_list = getattr(self, "module_list", None)
        if user_selected_module_list is None:
            return module_class_list

        filtered_module_list = []
        for module_class in module_class_list:
            module_class_name = module_class.__name__
            if module_class_name in user_selected_module_list:
                filtered_module_list.append(module_class)
        return filtered_module_list

    def http_request(
        self,
        request_type,
        url,
        headers=None,
        data="",
        files=None,
        check_expire=True,
        retry=True,
        check_token_timeout=True,
    ):

        if headers is None:
            headers = self.secHeaders

        if request_type == 'GET':
            res = self.session.get(
                                    url,
                                    headers=headers,
                                    data=data,
                                    verify=False
                                    )
        elif request_type == 'PUT':
            res = self.session.put(
                                    url,
                                    headers=headers,
                                    data=data,
                                    verify=False
                                    )
        elif request_type == 'POST':
            res = self.session.post(
                                    url,
                                    headers=headers,
                                    data=data,
                                    files=files,
                                    verify=False
                                    )
        elif request_type == 'DELETE':
            res = self.session.delete(
                                        url,
                                        headers=headers,
                                        data=data,
                                        verify=False
                                        )
        else:
            err_msg = 'The request type {} is not one of ' \
                      '["GET", "PUT", "POST", "DELETE"]'.format(request_type)
            raise Exception(err_msg)

        if not retry:
            return res

        if check_expire:
            try:
                res_content = res.content
                try:
                    res_content = res_content.decode()
                except Exception as e:
                    "{}".format(e)
                    pass

                # if "Wait for some time and try again " \
                #    "or contact Administrator" in res.text:
                if 'Content-Type' in res.headers and \
                    'text/html' in res.headers['Content-Type'] and \
                    '/logout' not in url and \
                    'id="errorMessageBox"' in res_content:
                    self._relogin()
                    new_headers = copy.deepcopy(self.secHeaders)
                    for key, value in headers.items():
                        if key not in new_headers:
                            new_headers[key] = value
                    return self.http_request(
                                                request_type=request_type,
                                                url=url,
                                                headers=new_headers,
                                                data=data,
                                                files=files,
                                                check_expire=False,
                                                retry=False
                                            )
            except Exception as e:
                print(e)
                # pass

        if check_token_timeout:
            try:
                if res.status_code == 403:
                    token_invalid_msg = "Token provided via HTTP Header does not match the token generated by the server"
                    if token_invalid_msg in res.text:
                        self._relogin()
                        new_headers = copy.deepcopy(self.secHeaders)
                        for key, value in headers.items():
                            if key not in new_headers:
                                new_headers[key] = value
                        return self.http_request(
                                                    request_type=request_type,
                                                    url=url,
                                                    headers=new_headers,
                                                    data=data,
                                                    files=files,
                                                    check_expire=False,
                                                    retry=False,
                                                    check_token_timeout=False
                                                )
            except Exception as e:
                print(e)
                # pass
        return res

    def login(self):
        """
        If login with user admin and password must be changed to do further operations is required. Do as the following!
            rest_session = VmanageAPI(ip="10.0.1.32", username="admin", password="admin", port=8443, new_password="Login_999")
        """
        ret = self._relogin()
        if ret is not None:
            new_password = getattr(self, "new_password", None)
            if "password_need_changed" in ret[1] and new_password:
                self._change_admin_password(self.password, new_password)
                self.password = self.new_password
                ret = self._relogin()
                if ret is not None:
                    print("{}, status_code: {}, error message: ".format(self.ip, ret.status_code, ret.text))
                    raise Exception("Change admin password failed for vmanage {}".format(self.ip))
            elif "password_need_changed" in ret[1]:
                raise Exception("Change {} password is required for vmanage {}".format(self.username, self.ip))

    def relogin(self, org_name=None):
        self._relogin(org_name)
        self.org_name = org_name

    def _relogin(self, org_name=None):
        network_reachability = tcp_port_alive(self.ip, self.port)
        if not network_reachability[0]:
            raise Exception("{}:{} is unreachable right now, Exit!".format(self.ip, self.port))

        self.secHeaders = {}
        self.session = requests.session()
        loginUrl = 'https://{}:{}/jts/authenticated/j_security_check' \
                   .format(self.ip, self.port)
        loginHeaders = {'Content-Type': 'application/x-www-form-urlencoded'}
        loginData = {'j_username': self.username,
                     'j_password': self.password
                     }

        login_response = self.session.post(
                                            loginUrl,
                                            data=loginData,
                                            headers=loginHeaders,
                                            verify=False
                                            )

        if 'Set-Cookie' not in login_response.headers:
            print(login_response.headers)
            raise Exception("Get auth header failed, "
                            "it might be incorrect username/password")
        token_session = self.session.get(
                                       'https://{}:{}'
                                       '/dataservice/client/server'
                                       .format(
                                               self.ip,
                                               self.port
                                               ),
                                       headers=None,
                                       verify=False
                                       )
        if token_session.status_code != 200:
            print("status_code: {}".format(token_session.status_code))
            print("error message: {}".format(token_session.text))
            raise Exception("Fail to get Token")
        else:
            if '"errorMessageBox"' in token_session.text and "Access Forbidden for this user" in token_session.text:
                raise Exception("User: {} might be locked or credentials incorrect for vmanage: {}".format(self.username, self.ip))
            elif all(['"errorMessageBox"' in token_session.text, 'Confirm Password' in token_session.text, 'New Password' in token_session.text, 'j_password' in token_session.text]):
                api = "/dataservice/client/token"
                url = 'https://{}:{}{}'.format(self.ip, self.port, api)
                ret = self.http_request("GET", url, headers=None)
                if ret.status_code == 200:
                    x_xsrf_token = ret.text
                    try:
                        x_xsrf_token = x_xsrf_token.encode()
                    except Exception as e:
                        "{}".format(e)

                    self.secHeaders['Cookie'] = login_response.headers['Set-Cookie'].split(';')[0]
                    self.secHeaders['Content-Type'] = 'application/json'
                    self.secHeaders['Accept'] = 'application/json, text/plain, */*'
                    self.secHeaders['X-XSRF-TOKEN'] = x_xsrf_token

                    return [False, {"password_need_changed": True}]
                else:
                    raise Exception("Get Token Failure for {}, password needs to be changed".format(self.ip))
            elif '"errorMessageBox"' in token_session.text:
                raise Exception("Get Token Failure for user: {} for vmanage: {}".format(self.username, self.ip))
            else:
                x_xsrf_token = token_session.json()['data']['CSRFToken']

        self.secHeaders['Cookie'] = login_response.headers['Set-Cookie'].split(';')[0]
        self.secHeaders['Content-Type'] = 'application/json'
        self.secHeaders['Accept'] = 'application/json, text/plain, */*'
        self.secHeaders['X-XSRF-TOKEN'] = x_xsrf_token

        if self.is_mtt:
            if org_name is None:
                org_name = self.org_name
                if not org_name:
                    raise Exception("org_name is not found!")

            ret = self._get_tenants_list()
            if not ret[0]:
                raise Exception("{}: Fail to get tenant list, msg: {}".format(self.ip, ret[1]))

            tenant_lists = ret[1]
            if org_name not in tenant_lists:
                raise Exception("org_name: {} is not found in: {}".format(org_name, tenant_lists))

            tenant_id = tenant_lists[org_name]['tenantId']
            ret = self._get_tenant_vsessionid(tenant_id)
            if not ret[0]:
                raise Exception("{}: Fail to get tenant_vsessionid, msg: {}".format(self.ip, ret[1]))

            self.secHeaders['VSessionId'] = ret[1]['VSessionId']

    def _change_admin_password(self, old_password, new_password):
        api = '/dataservice/admin/user/admin/password'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        payload = {'oldpassword': old_password, 'newpassword': new_password}
        ret = self.http_request("POST", url, data=json.dumps(payload))
        if ret.status_code != 200:
            print("{}, status_code: {}, error message: {}".format(self.ip, ret.status_code, ret.text))
            raise Exception("Fail to reset admin password for {}".format(self.ip))

    def _get_tenant_vsessionid(self, tenant_id):
        api = '/dataservice/tenant/{}/vsessionid'.format(tenant_id)
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("POST", url)

        if ret.status_code != 200:
            return [False, ret.text]
        else:
            return [True, ret.json()]

    def _get_tenants_list(self):
        api = '/dataservice/tenant'
        url = 'https://{}:{}{}'.format(self.ip, self.port, api)
        ret = self.http_request("GET", url)

        if ret.status_code != 200:
            return [False, ret.text]
        else:
            tenant_data = ret.json()['data']
            tenant_list = {}
            for tenant in tenant_data:
                tenant_list[tenant['orgName']] = tenant
            return [True, tenant_list]

    def load_extension(self, attr, module_path=None):
        module_path = os.getcwd() if module_path is None else module_path

        extension_file = "vmanage_" + attr + ".py"
        script_location = os.path.realpath(module_path)
        abs_extension_file = os.path.join(script_location, extension_file)
        if not os.path.isfile(abs_extension_file):
            raise AttributeError("Extension File '{}' is not found".format(abs_extension_file))

        if PY2:
            extension_module = imp.load_source(attr, abs_extension_file)
        else:
            spec = importlib.util.spec_from_file_location(attr, abs_extension_file)
            extension_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(extension_module)

        importted_class = getattr(extension_module, "Extension")
        for _attr in dir(importted_class):
            if "__" in _attr:
                continue
            function = getattr(importted_class, _attr)
            if PY2:
                try:
                    function = function.__func__
                except:
                    pass

            if isinstance(function, types.FunctionType):
                bound_method = function.__get__(self, self.__class__)
                setattr(self, "{}_".format(attr) + function.__name__, bound_method)

    def list_all_methods(self, key_word=None, regrex=False):
        if key_word:
            print("All available methods with keyword: '{}'".format(key_word))
        else:
            print("All available methods:")
        for attr in dir(self):
            if "__" in attr:
                continue
            ins = getattr(self, attr)
            if isinstance(ins, types.MethodType):
                if not key_word:
                    print("  {}".format(attr))
                    continue

                if regrex:
                    if re.search(key_word, attr):
                        print("  {}".format(attr))
                else:
                    if key_word in attr:
                        print("  {}".format(attr))

    def get_file(self, attr, print_error=False):
        try:
            ins_attr = getattr(self, attr)
        except Exception as e:
            print("Method: {} is not found".format(attr))
            if print_error:
                print("Error Message: {}".format(e))
            return

        try:
            file_location = inspect.getfile(ins_attr)
        except Exception as e:
            print("Error to get Method definition file")
            if print_error:
                print("Error Message: {}".format(e))
            return

        print("Definition File: {}".format(file_location))

    def get_log(self, attr):
        attr = os.path.basename(attr)
        script_location = os.path.dirname(os.path.realpath(__file__))
        api_log_location_files = os.path.join(script_location, "api_data/*")

        file_name_list = []
        for file_location in glob.glob(api_log_location_files):
            if not os.path.isfile(file_location):
                continue

            file_basename = os.path.basename(file_location)
            if attr in file_basename:
                file_name_list.append(file_basename)

        if file_name_list:
            print("Totally found {} files:".format(len(file_name_list)))
            for file_name in file_name_list:
                print("  {}".format(file_name))
        else:
            print("No file found.")

    def show_log(self, file_name):
        file_name = os.path.basename(file_name)
        script_location = os.path.dirname(os.path.realpath(__file__))
        api_log_location_file = os.path.join(script_location, "api_data", file_name)

        if not os.path.isfile(api_log_location_file):
            print("{} does not exists!".format(api_log_location_file))
            return

        print("# Show file Content: {}".format(api_log_location_file))
        with open(api_log_location_file, "r") as f:
            content = f.read()

        for line in content.splitlines():
            print(line)
