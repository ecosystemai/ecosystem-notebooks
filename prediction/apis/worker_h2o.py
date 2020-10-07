from prediction.endpoints import worker_h2o as endpoints
from prediction import request_utils

def train_model(auth, modelid, modeltype, params):
    ep = endpoints.BUILD_MODEL
    param_dict = {"model_id": modelid, "model_type": modeltype, "model_parms": params}
    resp = request_utils.create(auth, ep, params=param_dict)
    result = resp
    # result = resp.json()
    return result

def cancel_job(auth, jobid):
    ep = endpoints.CANCEL_JOB
    param_dict = {"job_id": jobid}
    resp = request_utils.create(auth, ep, params=param_dict)
    result = resp.json()
    return result

def delete_frame(auth, frame):
    ep = endpoints.DELETE_FRAME
    param_dict = {"frame": frame}
    resp = request_utils.create(auth, ep, params=param_dict)
    result = resp.json()
    return result

def download_model_mojo(auth, modelid):
    ep = endpoints.DOWNLOAD_MODEL_MOJO
    param_dict = {"model_id": modelid}
    resp = request_utils.create(auth, ep, params=param_dict)
    result = resp.json()
    return result

def get_train_model(auth, modelid, modeltype):
    ep = None
    if modeltype == "AUTOML":
        ep = endpoints.GET_AUTO_ML_MODEL
    else:
        ep = endpoints.GET_MODEL
    param_dict = {"model_id": modelid}
    resp = request_utils.create(auth, ep, params=param_dict)
    result = resp.json()
    return result

def get_frame(auth, frameid):
    ep = endpoints.GET_FRAME
    param_dict = {"frame_id": frameid}
    resp = request_utils.create(auth, ep, params=param_dict)
    result = resp.json()
    return result

def get_frame_columns(auth, frameid):
    ep = endpoints.GET_FRAME_COLUMNS
    param_dict = {"frame_id": frameid}
    resp = request_utils.create(auth, ep, params=param_dict)
    result = resp.json()
    return result

def get_model_stats(auth, modelid, source, statstype):
    ep = endpoints.GET_MODEL_STATS
    param_dict = {"model_id": modelid, "source": source, "stats_type": statstype}
    resp = request_utils.create(auth, ep, params=param_dict)
    result = resp.json()
    return result

def model_grids(auth, model):
    ep = endpoints.MODEL_GRIDS
    param_dict = {"model": model}
    resp = request_utils.create(auth, ep, params=param_dict)
    result = resp.json()
    return result

def prediction_frames(auth):
    ep = endpoints.PREDICTION_FRAMES
    resp = request_utils.create(auth, ep)
    result = resp.json()
    return result

def prediction_jobs(auth):
    ep = endpoints.PREDICTION_JOBS
    resp = request_utils.create(auth, ep)
    result = resp.json()
    return result

def prediction_models(auth):
    ep = endpoints.PREDICTION_MODELS
    resp = request_utils.create(auth, ep)
    result = resp.json()
    return result

def file_to_frame(auth, file_name, first_row_column_names, separator):
    ep = endpoints.PROCESS_FILE_TO_FRAME_IMPORT
    param_dict = {"file_name": file_name, "first_row_column_names": first_row_column_names, "separator": separator}
    resp = request_utils.create(auth, ep, params=param_dict)
    result = resp.json()
    return result

def featurestore_to_frame(auth, userframe):
    ep = endpoints.PROCESS_TO_FRAME_PARSE
    resp = request_utils.create(auth, ep, json=userframe)
    parsed_frame = resp.json()
    return parsed_frame
    
def split_frames(auth, frame, ratio):
    ep = endpoints.SPLIT_FRAMES
    param_dict = {"frame": frame, "ratio": ratio}
    resp = request_utils.create(auth, ep, params=param_dict)
    result = resp.json()
    return result