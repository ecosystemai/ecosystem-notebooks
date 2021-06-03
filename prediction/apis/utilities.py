from prediction.endpoints import utilities as endpoints
from prediction import request_utils

def convert_json_to_yaml(auth, json):
	ep = endpoints.CONVERT_JSON_TO_YAML
	resp = request_utils.create(auth, ep, json=json)
	yaml = resp.json()
	return yaml

def convert_range_from_to(auth, rules, value):
	ep = endpoints.CONVERT_RANGE_FROM_TO
	param_dict = {
		"rules": rules,
		"value": value
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def convert_text_file_from_to(auth, in_delimiter, in_file, out_delimiter, out_file, rules):
	ep = endpoints.CONVERT_TEXT_FILE_FROM_TO
	param_dict = {
		"inDelimiter": in_delimiter,
		"inFile": in_file,
		"outDelimiter": out_delimiter,
		"outFile": out_file,
		"rules": rules
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def convert_json_to_yaml(auth, yaml):
	ep = endpoints.CONVERT_YAML_TO_JSON
	resp = request_utils.create(auth, ep, json=yaml)
	json = resp.json()
	return json

def copy_file(auth, f_from, f_to):
	ep = endpoints.COPY_FILE
	param_dict = {
		"from": f_from,
		"to": f_to
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp
	return result

def get_file(auth, file_name, lines):
	ep = endpoints.GET_FILE
	param_dict = {
		"file": file_name,
		"lines": lines
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def execute_generic(auth, script):
	ep = endpoints.EXECUTE_GENERIC
	resp = request_utils.create(auth, ep, data=script)
	result = resp.json()
	return result