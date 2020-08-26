from runtime.apis import runtime_engine

class Authenticate:
	def __init__(self, api_address):
		self.api_address = api_address
		self.auth_headers = {
			"Accept": "*/*"
		}
		message = "Login Successful"
		output = runtime_engine.no_auth_ping(api_address, "/ping", self.auth_headers, message)
		if output["pong"] == message:
			print("Login Successful")
		else:
			print("Login Not Successful")

	def get_server(self):
		return self.api_address

	def get_auth_headers(self):
		return self.auth_headers