from os import listdir
from os.path import isfile, join
import sys
import json
import os
from glob import glob

prediction_server_path = "C:/Users/Ramsay/Documents/GitHub/ecosystem-server/"
prediction_fp = prediction_server_path + "src/main/java/com/ecosystem/"
# files = [f for f in listdir(prediction_fp) if isfile(join(prediction_fp, f))]
files = [y for x in os.walk(prediction_fp) for y in glob(os.path.join(x[0], "*.java"))]

server_endpoints = []
api_request = "@RequestMapping"
api_post_request = "@PostMapping"
api_get_request = "@GetMapping"

def stripping(parameter):
	if parameter[0] == "=":
		parameter = parameter[1:]
	parameter = parameter.replace("'", "")
	parameter = parameter.replace('"', "")
	if parameter[0] == ":":
		parameter = parameter[1:]
	return parameter

def create_endpoint(endpoint, method):
	d = {
		"endpoint": endpoint,
		"method": method
	}
	return d

def endpoints_equal(eps, epw):
	if eps == epw:
		return True
	if epw[-1] == "/":
		index1 = eps.find("{")
		index2 = eps.find("}")
		new_eps = eps[:index1] + eps[index2+1:]
		if new_eps == epw:
			return True
	return False

def compare_endpoints(server_endpoints, wrapper_endpoints):
	both = []
	server = []
	wrapper = []
	for d in server_endpoints:
		se = d["endpoint"]
		sm = d["method"]
		found = False
		for d2 in wrapper_endpoints:
			we = d2["endpoint"]
			wm = d2["method"]
			if endpoints_equal(se, we) and wm.lower() in sm.lower():
				both.append([d, d2])
				found = True
				break
		if not found:
			server.append(d)
	for d2 in wrapper_endpoints:
		we = d2["endpoint"]
		wm = d2["method"]
		found = False
		for d in server_endpoints:
			se = d["endpoint"]
			sm = d["method"]
			if endpoints_equal(se, we) and wm.lower() in sm.lower():
				found = True
				break
		if not found:
			wrapper.append(d2)

	print("")
	print("Found in both:")
	data = [
		["----SERVER----", "", "", "----WRAPPER----", ""],
		["method", "endpoint", "", "method", "endpoint"],
		["------", "------", "------", "------", "------"]
	]
	for b in both:
		row = [b[0]["method"], b[0]["endpoint"], "|", b[1]["method"], b[1]["endpoint"]]
		data.append(row)
	col_width = max(len(word) for row in data for word in row) + 2
	for row in data:
		print("".join(word.ljust(col_width) for word in row))
	print("Count:{}".format(len(both)))

	print("Only in one:")
	data = [
		["----SERVER----", ""],
		["method", "endpoint"],
		["------", "------"]
	]
	for s in server:
		row = [s["method"], s["endpoint"]]
		data.append(row)
	col_width = max(len(word) for row in data for word in row) + 2
	for row in data:
		print("".join(word.ljust(col_width) for word in row))
	print("Count:{}".format(len(server)))
	data = [
		["----WRAPPER----", ""],
		["method", "endpoint"],
		["------", "------"]
	]
	for w in wrapper:
		row = [w["method"], w["endpoint"]]
		data.append(row)
	col_width = max(len(word) for row in data for word in row) + 2
	for row in data:
		print("".join(word.ljust(col_width) for word in row))
	print("Count:{}".format(len(wrapper)))

for file_path in files:
	f = open(file_path, "r")
	endpoint_prefix = ""
	for line in f:
		if api_request in line:
			index = line.find(api_request)
			comment_index = line.find("//")
			if index != -1:
				if comment_index != -1:
					if comment_index < index:
						continue
				value = ""
				method = ""
				parameters = line[index+len(api_request):]
				endpoint_prefix = parameters[2:-3]
				parameters = parameters.split(",")
				for parameter in parameters:
					parameter = "".join(parameter.split())
					if "value" in parameter:
						if parameter[0] == "(":
							parameter = parameter[1:]
						if parameter[-1] == ")":
							parameter = parameter[:-1]
						index = parameter.find("value")
						parameter = parameter[index+len("value"):]
						value = stripping(parameter)

					elif "method" in parameter:
						if parameter[0] == "(":
							parameter = parameter[1:]
						if parameter[-1] == ")":
							parameter = parameter[:-1]
						index = parameter.find("method")
						parameter = parameter[index+len("method"):]
						method = stripping(parameter)
				if value != "" and method != "":
					server_endpoints.append(create_endpoint(value, method))
		if api_post_request in line:
			index = line.find(api_post_request)
			line = line[index+len(api_post_request):]
			line = line[2:-3]
			if endpoint_prefix[0] == "/":
				server_endpoints.append(create_endpoint(endpoint_prefix + line, "POST"))
			else:
				server_endpoints.append(create_endpoint(line, "POST"))
		if api_get_request in line:
			index = line.find(api_get_request)
			line = line[index+len(api_get_request):]
			line = line[2:-3]
			if endpoint_prefix[0] == "/":
				server_endpoints.append(create_endpoint(endpoint_prefix + line, "GET"))
			else:
				server_endpoints.append(create_endpoint(line, "GET"))
			


# for se in server_endpoints:
# 	print(se)

# print("count: {}".format(len(server_endpoints)))


wrapper_endpoints = []

wrapper_path = "../"
wrapper_fp = wrapper_path + "endpoints/"
files = [f for f in listdir(wrapper_fp) if isfile(join(wrapper_fp, f))]
if "__init__.py" in files:
	files.remove("__init__.py")

for f_n in files:
	file_path = wrapper_fp + f_n
	f = open(file_path, "r")
	data = f.read()
	data = "".join(data.split())
	while True:
		index = data.find("{")
		if index == -1:
			break
		open_count = 0
		close_count = 0
		for i in range(len(data[index:])):
			c = data[i+index]
			if c == "}":
				close_count += 1
			if c == "{":
				open_count += 1
			if open_count == close_count:
				s = data[index: index+i+1]
				j_str = eval(s)
				# j_str = json.loads(s)
				wrapper_endpoints.append(create_endpoint(j_str["endpoint"], j_str["type"]))
				data = data[index+i:]
				break

# for we in wrapper_endpoints:
# 	print(we)

# print("count: {}".format(len(wrapper_endpoints)))

compare_endpoints(server_endpoints, wrapper_endpoints)