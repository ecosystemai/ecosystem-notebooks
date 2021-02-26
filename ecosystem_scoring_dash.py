import time		
import sys
import json
from runtime import access
from runtime.apis import worker_utilities
from IPython.display import HTML, display
import tabulate
import ipywidgets as widgets
from prediction import jwt_access
from prediction.apis import worker_file_service
from prediction.apis import data_management_engine
from prediction.apis import data_munging_engine
from prediction.apis import utilities


SPENDING_PERSONALITY = worker_utilities.get_spend_personality
FINANCIAL_WELLNESS = worker_utilities.get_financial_wellness

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

def upload_file_pred(auth, path, target_path):
	worker_file_service.upload_file(auth, path, "/data/" +  target_path)

def upload_import_pred(auth, path, target_path, database, feature_store, feature_store_file):
	upload_file_pred(auth, path, target_path)
	data_management_engine.csv_import(auth, database, feature_store, feature_store_file)


def save_file(bytes, name):
	f = open(name, "wb")
	f.write(bytes)


class ScoringDash():
	def __init__(self, runtime_url, pred_url, pred_username, pred_pass):
		self.auth = access.Authenticate(runtime_url)
		self.p_auth = jwt_access.Authenticate(pred_url, pred_username, pred_pass)
		self.use_cases = {}
		self.to_upload = {}

	def create_use_case(self, name, local_file_path, target_path, database, model, key_field, function, feature_store, feature_store_file, properties, additional=None, additional_file=None): 
		use_case = {
			"name": name,
			"local_file_path": local_file_path,
			"target_path": target_path,
			"database": database,
			"model": model,
			"key_field": key_field,
			"feature_store": feature_store,
			"feature_store_file": feature_store_file,
			"additional": additional,
			"additional_file": additional_file,
			"properties": properties,
			"function": function
		}
		self.use_cases[name] = use_case
		path = local_file_path + model
		upload_file_runtime(self.auth, path, target_path)
		path = local_file_path + feature_store_file
		upload_import_runtime(self.auth, path, target_path, database, feature_store, feature_store_file)
		upload_import_pred(self.p_auth, path, target_path, database, feature_store, feature_store_file)

		if additional != None and additional_file != None:
			path = local_file_path + additional_file
			upload_import_runtime(self.auth, path, target_path, database, additional, additional_file)

	def spaces_num(self, pre_str, total_spaces):
		pre_l = len(pre_str)
		size = total_spaces - pre_l
		if size < 1:
			size = 1
		return " "*(size*2)
	    
	def get_key_categories(self, use_case_name, find_text):
		use_case = self.use_cases[use_case_name]
		unique_values = self.get_unique_values(use_case["name"], use_case["key_field"], find_text)
		text_list = []
		for key in sorted(unique_values):
			text_list.append("{}:{}{}".format(key, self.spaces_num(key, 20), unique_values[key]))
		return text_list
	    
	def setup_use_case(self, use_case_name):
		use_case = self.use_cases[use_case_name]
		worker_utilities.update_properties(self.auth, use_case["properties"])
		worker_utilities.refresh(self.auth)
    
	def get_use_case_names(self):
		return list(self.use_cases.keys())

	def score(self, use_case, value):
		if type(value) == str:
			if represents_int(value):
				value = int(value)
			elif represents_float(value):
				value = float(value)
			else:
				value = value
		else:
			value = value
		self.setup_use_case(use_case)
		campaign = use_case
		sub_campaign = "Na"
		channel = "APP"
		params = "{}"
		userid = "test_user"
		return self.use_cases[use_case]["function"](self.auth, campaign, channel, value, params, sub_campaign, userid) 

	def get_unique_values(self, use_case_name, field, find):
		use_case = self.use_cases[use_case_name]
		database = use_case["database"]
		collection = use_case["feature_store"]
		categoryfield = field
		total_to_process = 100
		results = data_munging_engine.get_categories(self.p_auth, database, collection, categoryfield, find, total_to_process) 
		return results
	    
	def get_documents_for_key_value(self, use_case_name, value):
		use_case = self.use_cases[use_case_name]
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
		total_to_process = 10
		skip = 0
		results = data_management_engine.get_data(self.p_auth, database, collection, find, total_to_process, projections, skip) 
		return results

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

	def score_btn_eventhandler(self, obj):
		value = self.score_input.value
		self.label_upload.value = ""
		results = self.score(self.dropdown_case.value, value)
		print("got results")
		if len(results["final_result"]) == 0:
			self.label_upload.value = "Value: '{}' not found in feature store. Upload data.".format(value)
			self.tab.selected_index = 1
		else:
			self.text_area2.value = json.dumps(results, indent=2)
			self.tab.selected_index = 0

	def dropdown_case_eventhandler(self, change):
		self.dropdown_customer.unobserve(self.dropdown_customer_eventhandler, names="value")
		if change.new in self.get_use_case_names():
			self.dropdown_customer.options = []
		else:
			print("error")
		self.dropdown_customer.value = None
		self.dropdown_customer.observe(self.dropdown_customer_eventhandler, names="value")

	def dropdown_customer_eventhandler(self, change):
		if change.new != None:
			value = change.new
			c_val = value.split(":")[0]
			results = self.get_documents_for_key_value(self.dropdown_case.value, c_val)
			self.table_out.clear_output()
			with self.table_out:
				header = results[0].keys()
				rows =  [x.values() for x in results]
				display(HTML(tabulate.tabulate(rows, header, tablefmt="html")))

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

	def find_btn_eventhandler(self, obj):
		find_filter = self.find_input.value
		use_case_name = self.dropdown_case.value
		filtered_values = self.get_key_categories(use_case_name, find_filter)
		self.dropdown_customer.options = filtered_values

	def upload_btn_eventhandler(self, obj):
		file_name = self.upload_text_input.value
		content = self.upload_input.value[file_name]["content"]
		save_file(content, "test_" + file_name)
		self.to_upload["customers"] = "test_" + file_name
		self.label_upload_done.value = file_name + " uploaded."

	def upload_btn_eventhandler2(self, obj):
		file_name = self.upload_text_input2.value
		content = self.upload_input2.value[file_name]["content"]
		save_file(content, "test_" + file_name)
		self.to_upload["transactions"] = "test_" + file_name
		self.label_upload_done2.value = file_name + " uploaded."

	def upload_btn_eventhandler3(self, obj):
		file_name = self.upload_text_input3.value
		content = self.upload_input3.value[file_name]["content"]
		save_file(content, "test_" + file_name)
		self.to_upload["CTO"] = "test_" + file_name
		self.label_upload_done3.value = file_name + " uploaded."

	def process_upload_btn_eventhandler(self, obj):
		use_case = self.use_cases[self.dropdown_case.value]
		for fp in self.to_upload.keys():
			if fp == "customers":
				feature_store = "customers_upload"
				data_management_engine.drop_document_collection(self.p_auth, use_case["database"], feature_store)
				upload_import_pred(self.p_auth, self.to_upload[fp], "/", use_case["database"], feature_store, self.to_upload[fp])
			elif fp == "transactions":
				feature_store = "transactions_upload"
				data_management_engine.drop_document_collection(self.p_auth, use_case["database"], feature_store)
				upload_import_pred(self.p_auth, self.to_upload[fp], "/", use_case["database"], feature_store, self.to_upload[fp])
			elif fp == "CTO":
				feature_store = "CTO_upload"
				data_management_engine.drop_document_collection(self.p_auth, use_case["database"], feature_store)
				upload_import_pred(self.p_auth, self.to_upload[fp], "/", use_case["database"], feature_store, self.to_upload[fp])
			else:
				print("ERROR unreachable state.")

		mongo_url = "mongodb://ecosystem_user:EcoEco321@localhost:54445"
		destinations = "listOfDestinations.txt"
		db_name = "fnb"
		proc_tx_data = "transactions_upload"
		proc_customer_data = "customers_upload"
		cto_data = "CTO_upload"
		sample_tx_data_rollup = "transactions_rollup_test"
		sample_tx_data_rollup_norm = "transactions_rollup_normalise_test"
		script = 'python3 enrich_for_runtime.py "{}" "{}" "{}" "{}" "{}" "{}" "{}" "{}"'.format(mongo_url, destinations, db_name, proc_tx_data, proc_customer_data, cto_data, sample_tx_data_rollup, sample_tx_data_rollup_norm)
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
			time.sleep(5)
			print("{}/ {}".format(re_count, init_count))
	def reupload_btn_eventhandler(self, obj):
		pass