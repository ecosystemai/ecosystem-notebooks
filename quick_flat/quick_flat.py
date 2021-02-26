import pymongo
import json
import datetime
import pprint

class QuickFlat:
	def __init__(self):
		f = open("config.conf")
		config = json.loads(f.read())
		login = config["login"]
		login_string = "mongodb://{}:{}@{}:{}/".format(login["username"], login["password"], login["ip"], login["port"])
		self.client = pymongo.MongoClient(login_string)
		self.db = self.client[config["database"]]
		self.output_db = config["output_database"]
		self.output_col = config["output_collection"]
		self.root_col = config["root_collection"]
		self.connections = config["connections"]


	def _index_field(self, collection_name, field):
		col = self.db[collection_name]
		index_results = col.create_index(field)
		print(index_results)

	def _get_fields(self, collection_name):
		col = self.db[collection_name]
		cursor = col.find().limit(1)
		keys = None
		for doc in cursor:
			keys = list(doc.keys())
		keys.remove("_id")
		return keys

	def _generate_mongo_command(self, root_col):
		commands = []
		# commands.append({"$limit": 10000})
		project_command = {
			"$project": {
				"_id": 0
			}
		}
		for con in self.connections:
			self._index_field(con["collection"], con["foreign_field"])
			self._index_field(root_col, con["local_field"])
			commands.append({
				"$lookup": {
					"from": con["collection"],
					"localField": con["local_field"],
					"foreignField": con["foreign_field"],
					"as": con["collection"]
				}
			})
			commands.append({"$unwind": "${}".format(con["collection"])})
			fields = self._get_fields(con["collection"])
			fields.remove(con["foreign_field"])
			for field in fields:
				project_command["$project"]["{}_{}".format(con["collection"], field)] = "${}.{}".format(con["collection"], field)

		fields = self._get_fields(root_col)
		for field in fields:
			project_command["$project"][field] = 1

		commands.append(project_command)


		merge_command = {"$merge": {"into": {"db": self.output_db, "coll": self.output_col}}}
		commands.append(merge_command)

		return commands

	def flatten(self):
		pp = pprint.PrettyPrinter(indent=4)
		root_col = self.db[self.root_col]
		# pp.pprint(self._generate_mongo_command(self.root_col))
		results = root_col.aggregate(self._generate_mongo_command(self.root_col))
		# for r in results:
		# 	pp.pprint(r)


qf = QuickFlat()
qf.flatten()