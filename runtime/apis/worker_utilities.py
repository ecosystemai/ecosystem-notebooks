from runtime.endpoints import worker_utilities as endpoints
from runtime import request_utils

# Cassandra database select
def get_cassandra(auth, sql, c_type):
    ep = endpoints.GET_CASSANDRA
    param_dict = {
        "sql": sql, 
        "type": c_type
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

# Cassandra database version
def get_cassandra_version(auth, params):
    ep = endpoints.GET_CASSANDRA_VERSION
    param_dict = {
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

# Obtain log file: Retrive number of lines from file.
def get_file(auth, file_name, lines):
    ep = endpoints.GET_FILE
    param_dict = {
        "file": file_name, 
        "lines": lines
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

# Get IP of server.
def get_ip(auth):
    ep = endpoints.GET_IP
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta

# List all models.
def get_model_list(auth):
    ep = endpoints.GET_MODEL_LIST
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta

# Properties read for MOJO list
def get_properties_mojo_list(auth):
    ep = endpoints.GET_PROPERTIES_MOJO_LIST
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta

# Properties read for predict parameter
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

# Create matrix from transcation list from properties file as setup in budget tracker.
def list_to_matrix(auth, params):
    ep = endpoints.LIST_TO_MATRIX
    param_dict = {
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

# Create list from matrix, import csv file.
def matrix_to_list(auth, params):
    ep = endpoints.MATRIX_TO_LIST
    param_dict = {
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

# Pull message from Kafka topic
def pull_kafka_topic(auth, message, params):
    ep = endpoints.PULL_KAFKA_TOPIC
    param_dict = {
        "message": message, 
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

# Push predictor scored result onto Kafka
def push_kafka_topic(auth, message, params):
    ep = endpoints.PUSH_KAFKA_TOPIC
    param_dict = {
        "message": message, 
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

# Update properties: MOJO list.
def update_mojo_list(auth, params):
    ep = endpoints.UPDATE_MOJO_LIST
    param_dict = {
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

# Update properties: Predict param
def update_predict_param(auth, params):
    ep = endpoints.UPDATE_PREDICT_PARAM
    param_dict = {
        "params": params
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta