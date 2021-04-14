import requests
from prediction.endpoints import auth_controller as endpoints
from datetime import datetime
import time

def stringify_data(data):
	str_data = str(data).replace("'", '"') 	# API requires input data to be in string format and must use " for denoting key and value pairs. Python's
											# to string method uses ' as to indicate strings in the key value pairs.
	return str_data

class AuthenticationError(Exception):
	"""Exception raised for incorrect authentication details."""
	def __init__(self):
		message = "Username and Password combonation not valid."
		super().__init__(message)

class AuthenticationExpiry(Exception):
	"""Exception raised for expired authentication token."""
	def __init__(self, expiry):
		expiry_datetime = datetime.utcfromtimestamp(expiry).strftime("%Y-%m-%d %H:%M:%S")
		message = "Authentication token expired on {}. Please login again.".format(expiry_datetime)
		super().__init__(message)

class Authenticate:
	def __init__(self, api_address, username, password):
		self.api_address = api_address
		self.username = username
		self.password = password
		token = self.__login(api_address, username, password)
		self.access_token = token["access_token"]
		self.refresh_token = token["refresh_token"]
		self.expires_in = self.__format_time(token["expires_in"])

		self.auth_headers = {
			"Accept": "*/*",
			"Authorization": "Bearer {}".format(self.access_token)
		}

	def __login(self, api_address, username, password):
		header = {
			"Accept": "*/*",
			"Content-Type": "application/json"
		}

		data = {
			"email": username,
			"password": password
		}
			
		str_data = stringify_data(data) # Stringify dict: data need to be in string format
		r = requests.post("{}{}".format(api_address, endpoints.AUTH_LOGIN["endpoint"]), headers=header, data=str_data)
		if r.status_code == 403:
			raise AuthenticationError()
		token = r.json()["token"]
		print("Login Successful.")
		return token

	def __format_time(self, t):
		# unix time in jwt authentication process seems to be oddly formated.
		# this function aligns the jwt expiry time with the python unix time.
		front = str(t)[:-3]
		end = str(t)[-3:]
		return float(front + "." + end)

	def __token_expired(self):
		current_time = time.time()
		if current_time >= self.expires_in:
			raise AuthenticationExpiry(self.expires_in)
		return False

	def get_username(self):
		if not self.__token_expired():
			return self.username

	def get_password(self):
		if not self.__token_expired():
			return self.password

	def get_server(self):
		if not self.__token_expired():
			return self.api_address

	def get_access_token(self):
		if not self.__token_expired():
			return self.access_token

	def get_refresh_token(self):
		if not self.__token_expired():
			return self.refresh_token

	def get_expiry_date(self):
		if not self.__token_expired():
			return self.expires_in

	def get_auth_headers(self):
		if not self.__token_expired():
			return self.auth_headers