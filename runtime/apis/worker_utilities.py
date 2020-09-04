from runtime.endpoints import worker_utilities as endpoints
from runtime import request_utils

def get_cassandra(auth, sql, c_type):
    ep = endpoints.GET_CASSANDRA
    param_dict = {
        "sql": sql, 
        "type": c_type
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def get_cassandra_version(auth, params):
    ep = endpoints.GET_CASSANDRA_VERSION
    param_dict = {
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def get_file(auth, file_name, lines):
    ep = endpoints.GET_FILE
    param_dict = {
        "file": file_name, 
        "lines": lines
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def get_ip(auth):
    ep = endpoints.GET_IP
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta

def get_model_list(auth):
    ep = endpoints.GET_MODEL_LIST
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta

def get_properties_mojo_list(auth):
    ep = endpoints.GET_PROPERTIES_MOJO_LIST
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta

def get_properties_predict_param(auth):
    ep = endpoints.GET_PROPERTIES_PREDICT_PARAM
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta

def get_rest(auth, path):
    ep = endpoints.LIST_TO_MATRIX
    param_dict = {
        "path": path
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def list_to_matrix(auth, params):
    ep = endpoints.LIST_TO_MATRIX
    param_dict = {
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def matrix_to_list(auth, params):
    ep = endpoints.MATRIX_TO_LIST
    param_dict = {
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def pull_kafka_topic(auth, message, params):
    ep = endpoints.PULL_KAFKA_TOPIC
    param_dict = {
        "message": message, 
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def push_kafka_topic(auth, message, params):
    ep = endpoints.PUSH_KAFKA_TOPIC
    param_dict = {
        "message": message, 
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def update_mojo_list(auth, params):
    ep = endpoints.UPDATE_MOJO_LIST
    param_dict = {
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def update_predict_param(auth, params):
    ep = endpoints.UPDATE_PREDICT_PARAM
    param_dict = {
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta