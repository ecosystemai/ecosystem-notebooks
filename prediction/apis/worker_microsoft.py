from prediction.endpoints import worker_microsoft as endpoints
from prediction import request_utils

def get_anomaly(auth, string):
	ep = endpoints.GET_ANOMALY
	param_dict = {
		"string": string
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta