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


SPENDING_PERSONALITY = worker_utilities.get_spend_personality
FINANCIAL_WELLNESS = worker_utilities.get_financial_wellness


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
	worker_utilities.upload_file(auth, path, target_path)

def upload_import_runtime(auth, path, target_path, database, feature_store, feature_store_file):
	upload_file_runtime(auth, path, target_path)
	worker_utilities.file_database_import(auth, database, feature_store, feature_store_file)

def upload_file_pred(auth, data_path, path, target_path):
	worker_file_service.upload_file(auth, path, data_path + target_path)

def upload_import_pred(auth, data_path, path, target_path, database, feature_store, feature_store_file):
	upload_file_pred(auth, data_path, path, target_path)
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
		self.model_path = worker_file_service.get_property(self.p_auth, "user.deployed.models")
		self.use_cases = {}
		self.to_upload = {}

	def test_connection(self, usecase_name):
		use_case = self.use_cases[usecase_name]
		puuid = uuid.uuid4()
		pong = runtime_engine.ping(use_case["auth"], puuid)
		print(pong)
		if pong["pong"] == str(puuid):
			return True
		return False

	def upload_use_case_files(self, usecase_name, target_path, database, model_path, fs_path, feature_store, ad_path=None, additional=None):
		use_case = self.use_cases[usecase_name]
		feature_store_file = ntpath.basename(fs_path)
		upload_file_runtime(use_case["auth"], model_path, target_path)
		upload_import_runtime(use_case["auth"], fs_path, target_path, database, feature_store, feature_store_file)
		upload_import_pred(self.p_auth, self.data_path, fs_path, target_path, database, feature_store, feature_store_file)

		if additional != None:
			additional_file = ntpath.basename(ad_path)
			upload_import_runtime(use_case["auth"], ad_path, target_path, database, additional, additional_file)

	def read_use_cases(self):
		database = "profilesMaster"
		collection = "dashboards"
		find = {}
		total_to_process = 100000
		projections = {}
		skip = 0
		results = data_management_engine.get_data(self.p_auth, database, collection, find, total_to_process, projections, skip)

	def load_use_case(self, name, database, key_field, function, feature_store, properties, runtime_url): 
		use_case = {
			"name": name,
			"database": database,
			"key_field": key_field,
			"feature_store": feature_store,
			"properties": properties,
			"function": function,
			"runtime_url": runtime_url,
			"auth": access.Authenticate(runtime_url)
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
	# def get_key_categories(self, usecase_name, find_text):
	# 	use_case = self.use_cases[usecase_name]
	# 	unique_values = self.get_unique_values(use_case["name"], use_case["key_field"], find_text)
	# 	text_list = []
	# 	for key in sorted(unique_values):
	# 		value = {
	# 			"label": "{}:{}{}".format(key, self.spaces_num(key, 20), unique_values[key]),
	# 			"value": key
	# 		}
	# 		text_list.append(value)
	# 	return text_list
	    
	def setup_use_case(self, usecase_name):
		use_case = self.use_cases[usecase_name]
		worker_utilities.update_properties(use_case["auth"], use_case["properties"])
		worker_utilities.refresh(use_case["auth"])
    
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

	def setup_display(self):
		ucns = self.get_use_case_names()
		self.dropdown_case = widgets.Dropdown(options = ucns, value = ucns[0], layout=widgets.Layout(width="84%", left="13px"))
		self.dropdown_customer = widgets.Select(
			options=[],
			rows=10,
			disabled=False,
			layout=widgets.Layout(width="90%")
		)
		self.label_case = widgets.Label("Use Case", layout=widgets.Layout(width="90%"))
		self.label_customer = widgets.Label("Customer", layout=widgets.Layout(width="90%"))
		self.label_other = widgets.Label("Transactions", layout=widgets.Layout(width="90%"))
		self.text_area = widgets.Textarea(
			disabled=True,
			layout=widgets.Layout(width="90%", height="100%")
		)

		self.text_area2 = widgets.Textarea(
			disabled=True,
			layout=widgets.Layout(width="91%", height="95%", left="12px")
		)
		self.score_btn = widgets.Button(description="Score")
		self.score_input = widgets.Text(
			description="Score Value",
			disabled=False,
			layout=widgets.Layout(width="62%")
		)

		self.find_label = widgets.Label("Find Filter", layout=widgets.Layout(width="90%"))
		self.find_btn = widgets.Button(description="Filter", layout=widgets.Layout(width="50px"))
		self.find_input = widgets.Text(
			description="",
			value="{}",
			disabled=False,
			layout=widgets.Layout(width="69%")
		)

		self.label_upload = widgets.Label("", layout=widgets.Layout(width="100%"))
		self.label_upload_h1 = widgets.Label("Customer Data", layout=widgets.Layout(width="100%"))
		self.label_upload_h2 = widgets.Label("Transaction Data", layout=widgets.Layout(width="100%"))
		self.label_upload_h3 = widgets.Label("CTO", layout=widgets.Layout(width="100%"))
		self.upload_text_input = widgets.Text(
			description="",
			disabled=True,
			layout=widgets.Layout(width="90%")
		)
		self.upload_input = widgets.FileUpload(
			disabled=False,
			accept = "",
			multiple=True,
			layout=widgets.Layout(width="30px")
		)
		self.upload_text_input2 = widgets.Text(
			description="",
			disabled=True,
			layout=widgets.Layout(width="90%")
		)
		self.upload_input2 = widgets.FileUpload(
			disabled=False,
			accept = "",
			multiple=True,
			layout=widgets.Layout(width="30px")
		)
		self.upload_text_input3 = widgets.Text(
			description="",
			disabled=True,
			layout=widgets.Layout(width="90%")
		)
		self.upload_input3 = widgets.FileUpload(
			disabled=False,
			accept = "",
			multiple=True,
			layout=widgets.Layout(width="30px")
		)
		self.table_out = widgets.Output(layout=widgets.Layout(overflow_y="auto", overflow_x="auto", width="100%", height="100%"))
		self.upload_btn = widgets.Button(description="Upload")
		self.label_upload_done = widgets.Label("", layout=widgets.Layout(width="50%"))
		self.hbox_upload_btn = widgets.HBox([self.upload_btn, self.label_upload_done])
		self.upload_btn2 = widgets.Button(description="Upload")
		self.label_upload_done2 = widgets.Label("", layout=widgets.Layout(width="50%"))
		self.hbox_upload_btn2 = widgets.HBox([self.upload_btn2, self.label_upload_done2])
		self.upload_btn3 = widgets.Button(description="Upload")
		self.label_upload_done3 = widgets.Label("", layout=widgets.Layout(width="50%"))
		self.hbox_upload_btn3 = widgets.HBox([self.upload_btn3, self.label_upload_done3])
		self.process_upload_btn = widgets.Button(description="Process Uploads", layout=widgets.Layout(width="90%"))
		self.reupload_btn = widgets.Button(description="Re upload", layout=widgets.Layout(width="90%"))
		self.hbox_find = widgets.HBox([self.find_input, self.find_btn], layout=widgets.Layout(left="12px", width="90%")) 
		self.hbox_upload = widgets.HBox([self.upload_text_input, self.upload_input])
		self.hbox_upload2 = widgets.HBox([self.upload_text_input2, self.upload_input2])
		self.hbox_upload3 = widgets.HBox([self.upload_text_input3, self.upload_input3])
		self.vbox_upload = widgets.VBox([self.label_upload, self.label_upload_h1, self.hbox_upload, self.hbox_upload_btn, self.label_upload_h2, self.hbox_upload2, self.hbox_upload_btn2, self.label_upload_h3, self.hbox_upload3, self.hbox_upload_btn3, self.process_upload_btn, self.reupload_btn], layout=widgets.Layout(width="91%"))
		self.tab = widgets.Tab(layout=widgets.Layout(width="100%", height="90%"))
		self.tab.children = [self.text_area2, self.vbox_upload]
		self.tab.set_title(0, "Scoring")
		self.tab.set_title(1, "Upload")
		self.hb_btns = widgets.HBox([self.score_input, self.score_btn], layout=widgets.Layout(height="16%"))
		self.vbox = widgets.VBox([self.label_case, self.dropdown_case, self.find_label, self.hbox_find, self.label_customer, self.dropdown_customer],  layout=widgets.Layout(width="30%"))
		self.vbox2 = widgets.VBox([self.label_other, self.table_out],  layout=widgets.Layout(width="70%", height="400px"))
		self.hb = widgets.HBox([self.vbox, self.vbox2])
		self.hb2 = widgets.HBox([self.tab], layout=widgets.Layout(height="90%", width="100%"))
		self.vbox_bot = widgets.VBox([self.hb_btns, self.hb2], layout=widgets.Layout(width="100%", height="600px"))
		# vbox3 = widgets.VBox([self.hb, self.hb2])

		self.dropdown_case.observe(self.dropdown_case_eventhandler, names="value")
		self.dropdown_customer.observe(self.dropdown_customer_eventhandler, names="value")
		self.score_btn.on_click(self.score_btn_eventhandler)
		self.find_btn.on_click(self.find_btn_eventhandler)
		self.upload_input.observe(self.upload_selector_eventhandler)
		self.upload_input2.observe(self.upload_selector_eventhandler2)
		self.upload_input3.observe(self.upload_selector_eventhandler3)
		self.upload_btn.on_click(self.upload_btn_eventhandler)
		self.upload_btn2.on_click(self.upload_btn_eventhandler2)
		self.upload_btn3.on_click(self.upload_btn_eventhandler3)
		self.process_upload_btn.on_click(self.process_upload_btn_eventhandler)
		self.reupload_btn.on_click(self.reupload_btn_eventhandler)

		return self.hb, self.vbox_bot

	def score_btn_eventhandler(self, usecase, score_value):
		svs = score_value.split(",")
		results = []
		errors = []
		for sv in svs:
			sv = sv.strip()
			result = self.score(usecase, sv)
			if len(result["final_result"]) == 0:
				errors.append("Value: '{}' not found in feature store. Upload data.\n".format(sv))
			else:
				results.append(result)
		if len(errors) >= 1:
			return errors
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

	def get_properties(self):
		data_results = data_management_engine.get_data(self.p_auth, "profilesMaster", "dashboards", "{}", 1000000, "{}", 0)
		for entry in data_results:
			properties = entry["properties"]
			usecase_name = entry["usecase"]
			rurl = entry["runtime_url"]
			predictor, database, feature_store, key_field = extract_properties(properties)
			function = function_from_string(predictor)
			self.load_use_case(usecase_name, database, key_field, function, feature_store, properties, rurl)

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

		data_management_engine.drop_document_collection(self.p_auth, "profilesMaster", "dashboards")
		upload_import_pred(self.p_auth, self.data_path, "tmp/properties.csv", "/", "profilesMaster", "dashboards", "properties.csv")

	def upload_btn_eventhandler(self, path, filename, content):
		fp = path + filename
		save_coded_file(content, fp)
		self.to_upload["customers"] = [fp, filename]

	def upload_btn_eventhandler2(self, path, filename, content):
		fp = path + filename
		save_coded_file(content, fp)
		self.to_upload["transactions"] = [fp, filename]

	def upload_btn_eventhandler3(self, path, filename, content):
		fp = path + filename
		save_coded_file(content, fp)
		self.to_upload["CTO"] = [fp, filename]

	def process_upload_btn_eventhandler(self, usecase_name, tmp_file_path):
		use_case = self.use_cases[usecase_name]
		for fp in self.to_upload.keys():
			if fp == "customers":
				feature_store = "customers_upload"
				data_management_engine.drop_document_collection(self.p_auth, use_case["database"], feature_store)
				upload_import_pred(self.p_auth, self.data_path, self.to_upload[fp][0], "/", use_case["database"], feature_store, self.to_upload[fp][1])
			elif fp == "transactions":
				feature_store = "transactions_upload"
				data_management_engine.drop_document_collection(self.p_auth, use_case["database"], feature_store)
				upload_import_pred(self.p_auth, self.data_path, self.to_upload[fp][0], "/", use_case["database"], feature_store, self.to_upload[fp][1])
			elif fp == "CTO":
				feature_store = "CTO_upload"
				data_management_engine.drop_document_collection(self.p_auth, use_case["database"], feature_store)
				upload_import_pred(self.p_auth, self.data_path, self.to_upload[fp][0], "/", use_case["database"], feature_store, self.to_upload[fp][1])
			else:
				print("ERROR unreachable state.")

		file_location = self.data_path
		py_file = file_location + "enrich_for_runtime.py"
		mongo_url = "mongodb://ecosystem_user:EcoEco321@localhost:54445"
		destinations = file_location + "listOfDestinations.txt"
		db_name = "fnb"
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
		target_path = "/"
		feature_store_file = "to_upload.csv"
		upload_import_runtime(use_case["auth"], tmp_file_path, target_path, use_case["database"], use_case["feature_store"], feature_store_file)
		upload_import_pred(self.p_auth, self.data_path, tmp_file_path, target_path, use_case["database"], use_case["feature_store"], feature_store_file)
# 27787506