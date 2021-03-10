from prediction.endpoints import worker_file_service as endpoints
from prediction import request_utils

def upload_file(auth, path, target_path):
    ep = endpoints.UPLOAD_FILE
    fileFp = open(path, "rb")
    files = {"file": fileFp}
    data = {"path": target_path}
    resp = request_utils.create_only_auth_no_error(auth, ep, data=data, files=files)
    return resp

def update_properties(auth, properties):
    ep = endpoints.UPDATE_PROPERTIES
    resp = request_utils.create_only_auth(auth, ep, data=properties)
    return resp

def get_file_tail(auth, path, file_path, lines):
	ep = endpoints.GET_FILE_TAIL
	param_dict = {
		"file": file_path,
		"lines": lines,
		"path": path
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	data = resp.content.decode("utf-8")[1:-1]
	rows = data.split("\n")
	new_rows = []
	new_rows.append(rows[0])
	for i in range(1, len(rows)):
		row = rows[i]
		new_rows.append(row[2:])
	new_data = "\n".join(new_rows)
	return new_data

def get_property(auth, property_key):
	ep = endpoints.GET_PROPERTY
	param_dict = {
		"key": property_key
	}
	resp = request_utils.create_only_auth(auth, ep, params=param_dict)
	data = resp.content.decode("utf-8")
	return data