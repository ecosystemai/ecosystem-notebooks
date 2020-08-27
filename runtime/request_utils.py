import requests
from requests import RequestException

class RequestTypeError(Exception):
	"""Exception raised for non existant request type."""
	def __init__(self, t):
		message = "Non existant request type: {}.".format(t)
		super().__init__(message)

class ApiError(IOError):
	"""There was an ambiguous exception that occurred while handling your
		request.
		"""
	def __init__(self, *args, **kwargs):
		"""Initialize RequestException with `request` and `response` objects."""
		response = kwargs.pop('response', None)
		self.response = response
		self.request = kwargs.pop('request', None)
		if (response is not None and not self.request and
			hasattr(response, 'request')):
			self.request = self.response.request
			# super(RequestException, self).__init__(*args, **kwargs) TODO: this gives errors, might not be neccesay.
			super().__init__(*args, **kwargs)

def auto_format_params(d):
	s = ""
	for key in d:
		s += "{key}={{{key}}}&".format(key=key)
	return s.format(**d)

def get_type(t):
	if t == "get":
		return requests.get
	elif t == "post":
		return requests.post
	elif t == "put":
		return request.put
	elif t == "delete":
		return requests.delete
	elif t == "patch":
		return request.patch
	else:
		raise RequestTypeError(t)

def create(auth, endpoint, json=None, params=None, ep_arg=None):
	url_endpoint = auth.get_server() + endpoint["endpoint"]
	if ep_arg != None:
		url_endpoint = url_endpoint + ep_arg
	resp = None
	call_message = endpoint["call_message"].format(type=endpoint["type"], endpoint=endpoint["endpoint"])
	if json == None and params == None:
		print(call_message)
		resp = get_type(endpoint["type"])(url_endpoint, headers=auth.get_auth_headers())
	elif json == None:
		print(call_message + "?" + auto_format_params(params))
		resp = get_type(endpoint["type"])(url_endpoint, headers=auth.get_auth_headers(), params=params)
	elif params == None:
		print(call_message)
		resp = get_type(endpoint["type"])(url_endpoint, headers=auth.get_auth_headers(), json=json)
	else:
		raise Exception("Error: Unsupported state: Both json and params parameters passed to create() function.")
	if resp.status_code != 200:
		error_message = endpoint["error_message"].format(type=endpoint["type"], endpoint=endpoint["endpoint"], response_code=resp.status_code)
		print(error_message)
		raise ApiError(error_message, response=resp)
	return resp