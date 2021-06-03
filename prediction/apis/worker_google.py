from prediction.endpoints import worker_google as endpoints
from prediction import request_utils

def get_security(auth, path):
	ep = endpoints.GET_SECURITY
	param_dict = {
		"path": path
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def get_sentiment(auth, string):
	ep = endpoints.GET_SENTIMENT
	param_dict = {
		"string": string
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta