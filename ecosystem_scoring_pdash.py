import time		
import sys
import json
import base64
from runtime import access
from runtime.apis import worker_utilities
from runtime.apis import runtime_engine
from IPython.display import HTML, display
import tabulate
import ipywidgets as widgets
from prediction import jwt_access
from prediction.apis import worker_file_service
from prediction.apis import data_management_engine
from prediction.apis import data_munging_engine
from prediction.apis import utilities
import csv
import ntpath
import uuid
import datetime
from datetime import timezone

SPENDING_PERSONALITY = worker_utilities.get_spend_personality
FINANCIAL_WELLNESS = worker_utilities.get_financial_wellness


def get_utc_timestamp():
	return datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()

def function_from_string(s):
	if s == "wellness_score":
		return FINANCIAL_WELLNESS
	if s == "spending_personality":
		return SPENDING_PERSONALITY
	return None

def represents_int(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

def represents_float(s):
	try: 
		float(s)
		return True
	except ValueError:
		return False

def upload_file_runtime(auth, path, target_path):
	worker_utilities.upload_file(auth, path, str(target_path))

def upload_import_runtime(auth, path, target_path, database, feature_store, feature_store_file):
	upload_file_runtime(auth, path, target_path)
	worker_utilities.file_database_import(auth, database, feature_store, feature_store_file)

def upload_file_pred(auth, data_path, path):
	worker_file_service.upload_file(auth, path, str(data_path))

def upload_import_pred(auth, data_path, path, database, feature_store, feature_store_file):
	upload_file_pred(auth, data_path, path)
	data_management_engine.csv_import(auth, database, feature_store, feature_store_file)

def save_file_text(text, name):
	f = open(name, "w")
	f.write(text)

def save_file(contents, name):
	f = open(name, "wb")
	f.write(contents)

def decode_text(contents):
	content_type, content_string = contents.split(',')
	decoded = base64.b64decode(content_string)
	decoded_text = decoded.decode("UTF-8")
	return decoded_text

def save_coded_file(contents, name):
	content_type, content_string = contents.split(',')
	decoded = base64.b64decode(content_string)
	save_file(decoded, name)

def extract(content, start, end):
	start_index = content.find(start)
	end_index = content.find(end, start_index + len(start))
	value = content[start_index+len(start): end_index]
	return value

def extract_properties(properties):
	prop_start = "predictor.param.lookup={"
	prop_end = "}}"
	contents = extract(properties, prop_start, prop_end)

	p_start = "predictor:'"
	p_end = "'"
	predictor = extract(contents, p_start, p_end)

	d_start = "db:'"
	d_end = "'"
	database = extract(contents, d_start, d_end)

	t_start = "table:'"
	t_end = "'"
	table = extract(contents, t_start, t_end)

	l_start = "lookup:{"
	l_end = "}"
	lookup = extract(contents, l_start, l_end)

	k_start = "key:'"
	k_end = "'"
	key = extract(lookup, k_start, k_end)

	return predictor, database, table, key

class ScoringDash():
	def __init__(self, pred_url, pred_username, pred_pass):
		self.user = pred_username
		self.p_auth = jwt_access.Authenticate(pred_url, pred_username, pred_pass)
		self.data_path = worker_file_service.get_property(self.p_auth, "user.data")
		self.use_cases = {}
		# self.to_upload = {}

	def get_runtime_url(self, usecase_name):
		use_case = self.use_cases[usecase_name]
		return use_case["runtime_url"]

	def get_properties(self, usecase_name):
		use_case = self.use_cases[usecase_name]
		return use_case["properties"]

	def get_predictor_type(self, usecase_name):
		use_case = self.use_cases[usecase_name]
		return use_case["predictor"]

	def get_key_field(self, usecase_name):
		use_case = self.use_cases[usecase_name]
		return use_case["key_field"]

	def test_connection(self, usecase_name):
		use_case = self.use_cases[usecase_name]
		puuid = uuid.uuid4()
		pong = runtime_engine.ping(use_case["auth"], puuid)
		if pong["pong"] == str(puuid):
			return True
		return False

	def upload_use_case_files(self, usecase_name, database, model_path, fs_path, feature_store, ad_path=None, additional=None):
		use_case = self.use_cases[usecase_name]
		self.setup_use_case(usecase_name)
		feature_store_file = ntpath.basename(fs_path)
		if use_case["model_d_path"] == "" or use_case["model_d_path"] == None:
			upload_file_runtime(use_case["auth"], model_path, use_case["model_g_path"])
		else:
			upload_file_runtime(use_case["auth"], model_path, use_case["model_d_path"])
		upload_import_runtime(use_case["auth"], fs_path, use_case["data_path"], database, feature_store, feature_store_file)
		upload_import_pred(self.p_auth, self.data_path, fs_path, database, feature_store, feature_store_file)

		if additional != None:
			additional_file = ntpath.basename(ad_path)
			upload_import_runtime(use_case["auth"], ad_path, use_case["data_path"], database, additional, additional_file)

	def read_use_cases(self):
		database = "profilesMaster"
		collection = "dashboards"
		find = {}
		total_to_process = 100000
		projections = {}
		skip = 0
		results = data_management_engine.get_data(self.p_auth, database, collection, find, total_to_process, projections, skip)

	def load_use_case(self, name, database, key_field, predictor, feature_store, properties, runtime_url): 
		auth = access.Authenticate(runtime_url)
		function = function_from_string(predictor)
		use_case = {
			"name": name,
			"database": database,
			"key_field": key_field,
			"feature_store": feature_store,
			"properties": properties,
			"predictor": predictor,
			"function": function,
			"runtime_url": runtime_url,
			"auth": auth,
			"data_path": worker_utilities.get_property(auth, "user.data"),
			"model_d_path": worker_utilities.get_property(auth, "user.deployed.models"),
			"model_g_path": worker_utilities.get_property(auth, "user.generated.models")
		}
		self.use_cases[name] = use_case

	def spaces_num(self, pre_str, total_spaces):
		pre_l = len(pre_str)
		size = total_spaces - pre_l
		if size < 1:
			size = 1
		return "\t"*(size*2)
	  
	def get_key_categories(self, usecase_name, find_text):
		use_case = self.use_cases[usecase_name]
		unique_values = self.get_unique_values(use_case["name"], use_case["key_field"], find_text)
		text_list = []
		for key in sorted(unique_values):
			value = {
				"label": "{}".format(key),
				"value": key
			}
			text_list.append(value)
		return text_list  
	
	def setup_use_case_straight(self, auth, properties):
		worker_utilities.update_properties(auth, properties)
		worker_utilities.refresh(auth)

	def setup_use_case(self, usecase_name):
		use_case = self.use_cases[usecase_name]
		self.setup_use_case_straight(use_case["auth"], use_case["properties"])
    
	def get_use_case_names(self):
		return list(self.use_cases.keys())

	def score(self, usecase_name, value):
		if type(value) == str:
			if represents_int(value):
				value = int(value)
			elif represents_float(value):
				value = float(value)
			else:
				value = value
		else:
			value = value
		usecase = self.use_cases[usecase_name]
		self.setup_use_case(usecase_name)
		campaign = usecase["name"]
		sub_campaign = "Na"
		channel = "APP"
		params = "{}"
		userid = self.user
		# userid = "test_user"
		return usecase["function"](usecase["auth"], campaign, channel, value, params, sub_campaign, userid)

	def get_unique_values(self, usecase_name, field, find):
		use_case = self.use_cases[usecase_name]
		database = use_case["database"]
		collection = use_case["feature_store"]
		categoryfield = field
		total_to_process = 100
		results = data_munging_engine.get_categories(self.p_auth, database, collection, categoryfield, find, total_to_process) 
		return results
	    
	def get_documents_for_key_value(self, usecase_name, value):
		use_case = self.use_cases[usecase_name]
		database = use_case["database"]
		collection = use_case["feature_store"]
		field = use_case["key_field"]
		find = "{}"
		if type(value) == str:
			if represents_int(value) or represents_float(value):
				find = "{'" + field + "': " + value + "}"
			else:
				find = "{'" + field + "': '" + value + "'}"
		else:
			find = "{'" + field + "': " + str(value) + "}"    
		projections = "{}"
		total_to_process = 100
		skip = 0
		results = data_management_engine.get_data(self.p_auth, database, collection, find, total_to_process, projections, skip)
		for result in results:
			for key in result:
				value = result[key]
				if type(value) != str:
					result[key] = str(value)
		return results

	def get_documents_for_key_value_header(self, usecase_name, value):
		use_case = self.use_cases[usecase_name]
		database = use_case["database"]
		collection = use_case["feature_store"]
		field = use_case["key_field"]
		find = "{}"
		if type(value) == str:
			if represents_int(value) or represents_float(value):
				find = "{'" + field + "': " + value + "}"
			else:
				find = "{'" + field + "': '" + value + "'}"
		else:
			find = "{'" + field + "': " + str(value) + "}"    
		projections = "{}"
		total_to_process = 2
		skip = 0
		results = data_management_engine.get_data(self.p_auth, database, collection, find, total_to_process, projections, skip)
		columns = []
		for doc in results:
			for key in doc.keys():
				value = {
					"name": key,
					"id": key
				}
				columns.append(value)
			break
		return columns

	def score_btn_eventhandler(self, usecase, score_value):
		svs = score_value.split(",")
		results = []
		errors = []
		for sv in svs:
			sv = sv.strip()
			result = self.score(usecase, sv)
			if len(result["final_result"]) == 0:
				errors.append(sv)
			else:
				kf_data = self.dropdown_customer_eventhandler(sv, usecase)
				result["source_data"] = kf_data
				results.append(result)
		if len(errors) >= 1:
			raise Exception("Values: {} not found in featues store. Upload data.".format(errors))
		return json.dumps(results, indent=2)

	def dropdown_case_eventhandler(self, change):
		self.dropdown_customer.unobserve(self.dropdown_customer_eventhandler, names="value")
		if change.new in self.get_use_case_names():
			self.dropdown_customer.options = []
		else:
			print("error")
		self.dropdown_customer.value = None
		self.dropdown_customer.observe(self.dropdown_customer_eventhandler, names="value")

	def dropdown_customer_eventhandler(self, customer, usecase):
		results = self.get_documents_for_key_value(usecase, customer)
		return results

	def dropdown_customer_header_eventhandler(self, customer, usecase):
		results = self.get_documents_for_key_value_header(usecase, customer)
		return results

	def upload_selector_eventhandler(self, change):
		if len(self.upload_input.value) != 0:
			filenames = []
			for key in self.upload_input.value.keys():
				filenames.append(key)
			self.upload_text_input.value = "; ".join(filenames)

	def upload_selector_eventhandler2(self, change):
		if len(self.upload_input2.value) != 0:
			filenames = []
			for key in self.upload_input2.value.keys():
				filenames.append(key)
			self.upload_text_input2.value = "; ".join(filenames)

	def upload_selector_eventhandler3(self, change):
		if len(self.upload_input3.value) != 0:
			filenames = []
			for key in self.upload_input3.value.keys():
				filenames.append(key)
			self.upload_text_input3.value = "; ".join(filenames)

	def find_btn_eventhandler(self, usecase_name, find_filter):
		filtered_values = self.get_key_categories(usecase_name, find_filter)
		return filtered_values

	def retrieve_properties(self):
		data_results = data_management_engine.get_data(self.p_auth, "profilesMaster", "dashboards", "{}", 1000000, "{}", 0)
		for entry in data_results:
			try:
				properties = entry["properties"]
				usecase_name = entry["usecase"]
				rurl = entry["runtime_url"]
				predictor, database, feature_store, key_field = extract_properties(properties)
				self.load_use_case(usecase_name, database, key_field, predictor, feature_store, properties, rurl)
			except:
				continue

	def preprocess_properties(self, usecase_name, runtime_url, properties):
		headers = ["usecase", "runtime_url", "properties"]
		l = [usecase_name, runtime_url, properties]
		data = [headers, l]
		data_results = data_management_engine.get_data(self.p_auth, "profilesMaster", "dashboards", "{}", 1000000, "{}", 0)
		for entry in data_results:
			usecase = entry["usecase"]
			rurl = entry["runtime_url"]
			prop = entry["properties"]
			data.append([usecase, rurl, prop])
		with open("tmp/properties.csv", "w", newline="") as f:
			writer = csv.writer(f)
			writer.writerows(data)
		predictor, database, feature_store, key_field = extract_properties(properties)
		auth = access.Authenticate(runtime_url)
		self.setup_use_case_straight(auth, properties)
		self.load_use_case(usecase_name, database, key_field, predictor, feature_store, properties, runtime_url)
		data_management_engine.drop_document_collection(self.p_auth, "profilesMaster", "dashboards")
		upload_import_pred(self.p_auth, self.data_path, "tmp/properties.csv", "profilesMaster", "dashboards", "properties.csv")


	def wellness_process_uploads(self, usecase_name, c_path, c_filename, c_content):
		c_fp = c_path + c_filename
		save_coded_file(c_content, c_fp)

		use_case = self.use_cases[usecase_name]

		upload_import_runtime(use_case["auth"], c_fp, use_case["data_path"], use_case["database"], use_case["feature_store"], c_filename)
		upload_import_pred(self.p_auth, self.data_path, c_fp, use_case["database"], use_case["feature_store"], c_filename)

	def spend_personality_process_uploads(self, usecase_name, tmp_file_path, c_path, c_filename, c_content, t_path, t_filename, t_content, cto_path, cto_filename, cto_content):
		c_fp = c_path + c_filename
		save_coded_file(c_content, c_fp)
		t_fp = t_path + t_filename
		save_coded_file(t_content, t_fp)
		cto_fp = cto_path + cto_filename
		save_coded_file(cto_content, cto_fp)

		use_case = self.use_cases[usecase_name]

		feature_store = "customers_upload"
		data_management_engine.drop_document_collection(self.p_auth, use_case["database"], feature_store)
		upload_import_pred(self.p_auth, self.data_path, c_fp, use_case["database"], feature_store, c_filename)
			
		feature_store = "transactions_upload"
		data_management_engine.drop_document_collection(self.p_auth, use_case["database"], feature_store)
		upload_import_pred(self.p_auth, self.data_path, t_fp, use_case["database"], feature_store, t_filename)
			
		feature_store = "CTO_upload"
		data_management_engine.drop_document_collection(self.p_auth, use_case["database"], feature_store)
		upload_import_pred(self.p_auth, self.data_path, cto_fp, use_case["database"], feature_store, cto_filename)

		file_location = self.data_path
		py_file = file_location + "enrich_for_runtime.py"
		mongo_url = "mongodb://ecosystem_user:EcoEco321@localhost:54445"
		destinations = file_location + "listOfDestinations.txt"
		db_name = use_case["database"]
		proc_tx_data = "transactions_upload"
		proc_customer_data = "customers_upload"
		cto_data = "CTO_upload"
		sample_tx_data_rollup = "transactions_rollup_test"
		sample_tx_data_rollup_norm = "transactions_rollup_normalise_test"
		script = "python3 {} {} {} {} {} {} {} {} {}".format(py_file, mongo_url, destinations, db_name, proc_tx_data, proc_customer_data, cto_data, sample_tx_data_rollup, sample_tx_data_rollup_norm)
		utilities.execute_generic(self.p_auth, script)
		init_count = 0
		results = data_management_engine.get_data(self.p_auth, use_case["database"], "customers_upload", "{}", 1000000, "{}", 0)
		for doc in results:
			init_count += 1
		while True:
			re_count = 0
			results = data_management_engine.get_data(self.p_auth, use_case["database"], "customers_upload", "{CTO: { $exists: true }}", 1000000, "{}", 0)
			for doc in results:
				re_count += 1
			if re_count >= init_count:
				break
			time.sleep(1)
		# re_upload
		filename = proc_customer_data + "_re.csv"
		filetype = "csv"
		field = "{}"
		sort = "{}"
		projection = "{}"
		limit = 0
		data_management_engine.export_documents(self.p_auth, filename, filetype, db_name, proc_customer_data, field, sort, projection, limit)
		path = self.data_path
		lines = 1000000
		content = worker_file_service.get_file_tail(self.p_auth, path, filename, lines)
		save_file_text(content, tmp_file_path)
		target_path = use_case["data_path"]
		feature_store_file = "to_upload.csv"
		upload_import_runtime(use_case["auth"], tmp_file_path, target_path, use_case["database"], use_case["feature_store"], feature_store_file)
		upload_import_pred(self.p_auth, self.data_path, tmp_file_path, use_case["database"], use_case["feature_store"], feature_store_file)
# 27787506