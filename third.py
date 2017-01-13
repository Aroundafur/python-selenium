#!/usr/bin/env python
import requests
import json
from datetime import datetime, timedelta


"""third.py, By Doron Smoliansky, 2017-1-10
program creates API call, and runs tests 3 tests:
1. valid requests that receive a valid response
2. Invalid request for timestamps out of range
3. Invalid request for threshold out of range
"""



class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
N = 14
rtoken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzY29wZXMiOlsicmlza19zY29yZSIsInJlc3RfYXBpIl0sImlhd\
CI6MTQ2MzQxNDY2NSwic3ViIjoiUFgyMDAzIiwianRpIjoiYjdjNTMwYzAtOWQwMy00YTJhLThlZGEtOTVk\
Y2U1NDliNmVhIn0.6EwE-m7eOJAaPbGYz2zR_1-7lvrtFR0rKLykwonZZjo"

def get(rtype = "socket_ip", rip_address = "81.82.81.82", url = 'http://portal-stg.perimeterx.com/report/v1/ip', start_time=1481718521000, end_time=1482928121000, threshold=60):
    """Returns the GET response, else throws exception

    >>> get("socket_ip", "81.82.81.82", 'http://portal-stg.perimeterx.com/report/v1/ip', 1481718521000, 1482928121000, 60)
    400

    >>> get("socket_ip", "81.82.81.82", 'http://portal-stg.perimeterx.com/report/v1/ip', 11481718521000, 1482928121000, 60)
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest __main__.get[1]>", line 1, in <module>
        get("socket_ip", "81.82.81.82", 'http://portal-stg.perimeterx.com/report/v1/ip', 11481718521000, 1482928121000, 60)
      File "third.py", line 35, in get
        if(validate_times(start_time, end_time) and validate_threshold(threshold)):
      File "third.py", line 82, in validate_times
        raise MyError("start_time and end_time - should be valid 13 digits timestamp")
    MyError: 'start_time and end_time - should be valid 13 digits timestamp'

    >>> get("socket_ip", "81.82.81.82", 'http://portal-stg.perimeterx.com/report/v1/ip', 1481718521000, 1482928121000, -555)
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest __main__.get[2]>", line 1, in <module>
        get("socket_ip", "81.82.81.82", 'http://portal-stg.perimeterx.com/report/v1/ip', 1481718521000, 1482928121000, -555)
      File "third.py", line 56, in get
        if(validate_times(start_time, end_time) and validate_threshold(threshold)):
      File "third.py", line 84, in validate_threshold
        raise MyError("threshold - number in the range of 0-100")
    MyError: 'threshold - number in the range of 0-100'


    """
    try:
        validate_times(start_time, end_time)
    except MyError as e:
         print e.value
    try:
        validate_threshold(threshold)
    except MyError as e:
        print e.value

    if(validate_times(start_time, end_time) and validate_threshold(threshold) and validate_type(rtype)and validate_value(rip_address)):
        headers = {
            'Authorization': 'Bearer ' + rtoken,
            "Content-Type": "application/json",
            'data':{
                "report": {
                "type": rtype,
                "value": rip_address,
                "time": {
                "type": "range",
                "start_time": start_time, "end_time": end_time
                },
                "threshold": threshold
                }
            }
        }
        print requests.get(url, data=json.dumps(headers['data']), headers=headers).status_code

def validate_type(rtype="socket_ip"):
    """Returns the True if the given type is valid, else return False.

    >>> validate_type("socket_ip")
    True
    >>> validate_type("forward_ip")
    True
    >>> validate_type("meow")
    False
    """
    types = ['socket_ip', 'forward_ip']
    if rtype in types:
        return True
    return False

def validate_value(rip_address="0.0.0.0"):
    """Returns the True if the value is a valid ip address, else return False.

    >>> validate_value("0.0.0.0")
    True
    >>> validate_value("woof")
    False

    """
    import socket
    try:
        socket.inet_aton(rip_address)
    except socket.error:
        return False
    else:
        return True

def validate_threshold(threshold=60):
    """Returns the True if the threshold is valid, else throw exception.

    >>> validate_threshold(60)
    True

    """
    if threshold > 0 and threshold < 100:
        return True
    else:
        raise MyError("threshold - number in the range of 0-100")


def validate_times(start_time=1481718521000, end_time=1482928121000):
    """Returns the True if the times are valid, else throw exception.

    >>> validate_times(1481718521000, 1482928121000)
    True
    """
    if len(str(start_time)) == len(str(end_time)):
        if len(str(start_time)) == 13:
            start_time = datetime(1970, 1, 1) + timedelta(milliseconds=start_time)
            end_time = datetime(1970, 1, 1) + timedelta(milliseconds=end_time)
            time_period = end_time - start_time
            if str(N)+" days" in str(end_time - start_time):
                return True
            else:
                raise MyError("period between start_time and end_time - should a 14 days period")
    else:
        raise MyError("start_time and end_time - should be valid 13 digits timestamp")



if __name__=="__main__":
    import doctest
    doctest.testmod()
