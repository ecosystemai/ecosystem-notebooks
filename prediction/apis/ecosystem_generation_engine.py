from endpoints import ecosystem_generation_engine as endpoints
import request_utils

def generate_build(auth, json):
    ep = endpoints.GENERATE_BUILD
    resp = request_utils.create(auth, ep, json=json)
    result = resp.json()
    return result

def generate_properties(auth, json):
    ep = endpoints.GENERATE_PROPERTIES
    resp = request_utils.create(auth, ep, json=json)
    result = resp.json()
    return result

def get_build(auth, uuid):
    ep = endpoints.GET_BUILD
    param_dict = {
        "uuid": uuid
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    if "data" in meta:
        meta = meta["data"]
    return meta

def process_build(auth, json):
    ep = endpoints.PROCESS_BUILD
    resp = request_utils.create(auth, ep, json=json)
    result = resp.json()
    return result