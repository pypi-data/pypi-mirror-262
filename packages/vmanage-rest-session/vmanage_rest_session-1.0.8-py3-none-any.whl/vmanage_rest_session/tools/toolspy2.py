import socket
import time
import os
import sys
from contextlib import contextmanager
from functools import wraps


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


@contextmanager
def suppress_log():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


def check_and_wait(
        expect_val,
        max_time,
        poll_time,
        return_raw=True,
        max_time_is_count=False,
        call_on_fail_func=None,
        *call_on_fail_func_args):
    def decorator(func):
        @wraps(func)
        def inner_func(*args, **kargs):
            if max_time_is_count:
                count = 0
                result = [False, 'Exceed Max Retry']
                while count < max_time:
                    ret = func(*args, **kargs)
                    if return_raw:
                        result = ret
                    if isinstance(ret, list):
                        if ret[0] == expect_val:
                            return ret
                        else:
                            count += 1
                    else:
                        if ret == expect_val:
                            return ret
                        else:
                            count += 1
                if call_on_fail_func is not None:
                    call_on_fail_func(*call_on_fail_func_args)
           
                return result
            else:
                start_time = time.time()
                result = [False, 'Not Sufficient Timeout']
                while time.time() - start_time < max_time:
                    ret = func(*args, **kargs)
                    if return_raw:
                        result = ret
                    if isinstance(ret, list):
                        if ret[0] == expect_val:
                            return ret
                        else:
                            time.sleep(poll_time)
                    else:
                        if ret == expect_val:
                            return ret
                        else:
                            time.sleep(poll_time)
                if call_on_fail_func is not None:
                    call_on_fail_func(*call_on_fail_func_args)

                return result
        return inner_func
    return decorator


@check_and_wait(True, 60, 1)
def tcp_port_alive(ip, port, print_message=True):
    timeout = 5
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return [True, "Connection is ok"]
    except BaseException:
        if print_message:
            print("{}:{} TCP connection checked failed, trying ...".format(ip, port))
        return [False, "connection is not ok"]
    finally:
        s.close()


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K
