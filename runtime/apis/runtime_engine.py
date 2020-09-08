from runtime.endpoints import runtime_engine as endpoints
from runtime import request_utils
import requests

# Get Login
def login(auth):
    ep = endpoints.LOGIN
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta

# Ping server and provide response
#   message: The message to return. (string)
def ping(auth, message):
    ep = endpoints.PING
    param_dict = {
        "message": message
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def no_auth_ping(server, endpoint, headers, message):
    url_endpoint = server + endpoint
    param_dict = {
        "message": message
    }
    resp = requests.get(url_endpoint, headers=headers, params=param_dict)
    meta = resp.json()
    return meta