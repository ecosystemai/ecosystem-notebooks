from os import listdir
from os.path import isfile, join
import sys
import json

runtime_server_path = "C:/Users/Ramsay/Documents/GitHub/ecosystem-runtime/"
runtime_fp = runtime_server_path + "src/main/java/com/ecosystem/runtime/"
files = [f for f in listdir(runtime_fp) if isfile(join(runtime_fp, f))]

server_endpoints = []
api_request = "@RequestMapping"
api_post_request = "@PostMapping"

def stripping(parameter):
	if parameter[0] == "=":
		parameter = parameter[1:]
	parameter = parameter.replace("'", "")
	parameter = parameter.replace('"', "")
	if parameter[0] == ":":
		parameter = parameter[1:]
	# if parameter[0] == '"' or parameter[0] == "'":
	# 	parameter = parameter[1:]
	# if parameter[-1] == '"' or parameter[-1] == "'":	
	# 	parameter = parameter[:-1]
	return parameter

def create_endpoint(endpoint, method):
	d = {
		"endpoint": endpoint,
		"method": method
	}
	return d

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
			if se == we and wm.lower() in sm.lower():
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
			if se == we and wm.lower() in sm.lower():
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

for f_n in files:
	file_path = runtime_fp + f_n
	f = open(file_path, "r")
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
				parameters = parameters.split(",")
				for parameter in parameters:
					parameter = "".join(parameter.split())
					if parameter[0] == "(":
						parameter = parameter[1:]
					if parameter[-1] == ")":
						parameter = parameter[:-1]
					if "value" in parameter:
						index = parameter.find("value")
						parameter = parameter[index+len("value"):]
						value = stripping(parameter)

					elif "method" in parameter:
						index = parameter.find("method")
						parameter = parameter[index+len("method"):]
						method = stripping(parameter)
						
				server_endpoints.append(create_endpoint(value, method))
		if api_post_request in line:
			index = line.find(api_post_request)
			line = line[index+len(api_post_request):]
			line = line[2:-3]
			server_endpoints.append(create_endpoint(line, "POST"))


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
	new_data = []
	for line in f:
		line = "".join(line.split())
		if len(line) > 0:
			if line[0] != "#":
				new_data.append(line)
	data = "".join(new_data)
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