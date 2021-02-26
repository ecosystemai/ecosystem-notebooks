import json
import pymongo

class Flattener:
	def __init__(self, config_path):
		f = open(config_path)
		config = json.loads(f.read())
		self.login = config["login"]
		self.login_string = "mongodb://{}:{}@{}:{}/".format(self.login["username"], self.login["password"], self.login["ip"], self.login["port"])
		self.database = config["database"]
		self.root = config["root_collection"]
		self.unique_threshold = config["unique_threshold"]
		self.output_database = config["output_database"]
		self.output_collection = config["output_collection"]
		self.client = pymongo.MongoClient(self.login_string)

	def _collection_list(self):
		self.collections = self.client[self.database].collection_names()

	def _check_field_is_key(self, collection_name):
		col = self.client[self.database][collection_name]
		cursor = col.find().limit(1)
		keys = None
		for doc in cursor:
			keys = list(doc.keys())
		keys.remove("_id")
		count = col.count_documents({})
		print(count)
		for key in keys:
			ag = col.aggregate([{"$group": {"_id": "${}".format(key)}}])
			dist_count = 0
			for d in ag:
				dist_count += 1
			# dist_count = len(col.distinct(key))
			percentage = dist_count / count
			print("{}: {}".format(key, percentage))


flat = Flattener("config.conf")
flat._check_field_is_key("tscm_account_transaction")


# 14secs for 10 000 records pre index