import pymongo
import json
import datetime
# for db in client.list_databases():
# 	print(db)


# cols = [
# 	"tscm_account_transaction",
# 	# "tscm_transaction_event_foreign",
# 	# "tscm_transaction_event_uk",
# 	"tsmf_contribution_transaction",
# 	"tsmf_investment_transaction",
# 	"tscm_event"
# ]
# for col in db.list_collection_names():
# 	if col in cols:
# 		print(col)

# tscm account transaction - username, transaciton type, tscm transaction type flattening, build network. Time user spend on transaction.*
# tsm transaction event foreain
# tsmf contribution transaction
# tsmf envestent transaction
# results = acc_trans.find().limit(1)
# for r in results:
# 	for k in r.keys():
# 		print("{}: {}".format(k, r[k]))

# results = acc_trans.find().limit(1)
# results = acc_trans.aggregate([{"$match": {"ACTR_TIMESTAMP": {"$gt": 20}}}, {"$limit": 2}])
# results = acc_trans.find({}, {"_id": 0, "ACTR_CLIENT_ID" : 1}).limit(1)
# for r in results:
# 	for k in r.keys():
# 		print("{}: {}".format(k, r[k]))

		
# client_col = db["tscm_client"]
# results = client_col.find({}, {"_id": 0, "CLNT_ID" : 1}).limit(1)
# for r in results:
# 	for k in r.keys():
# 		print("{}: {}".format(k, r[k]))

class TransactionReader:
	def __init__(self, batch_size):
		f = open("login.conf")
		login = json.loads(f.read())
		login_string = "mongodb://{}:{}@{}:{}/".format(login["username"], login["password"], login["ip"], login["port"])
		self.client = pymongo.MongoClient(login_string)

		# self.db = self.client["sonata_processed"]
		self.db = self.client["sonata"]
		self.batch_size = batch_size
		self.skip = 0 	#1241470

	def get_unique_users(self):
		db_other = self.client["sonata"]
		acc_trans = db_other["tscm_account_transaction"]
		return acc_trans.distinct("ACTR_LAST_UPDATED_BY")

	def get_unique_transaction_types(self):
		db_other = self.client["sonata"]
		trans_type = db_other["tscm_transaction_type"]
		return trans_type.distinct("TTYP_DESCRIPTION")

	def read(self):
		acc_trans = self.db["tscm_account_transaction"]
		# acc_trans = self.db["edges"]
		results = acc_trans.aggregate([
			{"$skip": self.skip},
			{"$limit": self.batch_size},
			# {"$project": {
			# 		"_id": 0,
			# 		"USER": 1,
			# 		"TYPE": 1,
			# 		"DATE_TIME": 1
			# 	}
			# }
			{
				"$lookup": {
					"from": "tscm_client",
					"localField": "ACTR_CLIENT_ID",
					"foreignField": "CLNT_ID",
					"as": "client"
				},
			},
			{"$unwind": "$client"},
			{
				"$lookup": {
					"from": "tscm_transaction_type",
					"localField": "ACTR_TRANSACTION_TYPE_ID",
					"foreignField": "TTYP_ID",
					"as": "type"
				},
			},
			{"$unwind": "$type"},
			{
				"$project": {
					"_id": 0,
					"DATE_TIME": "$ACTR_FINANCIAL_ACCT_PERIOD",
					"USER": "$ACTR_LAST_UPDATED_BY",
					# "NAME": {"$concat": ["$client.CLNT_SURNAME", ", ", "$client.CLNT_FORENAME"]},
					"TYPE": "$type.TTYP_DESCRIPTION"
				}
			}
			# {"$merge": {"db": "sonata_processed", "coll": "edges"}}
		])
		self.skip += self.batch_size
		return results

class FilteredTransactionReader:
	def __init__(self, batch_size, startdate, enddate, users):
		f = open("login.conf")
		login = json.loads(f.read())
		login_string = "mongodb://{}:{}@{}:{}/".format(login["username"], login["password"], login["ip"], login["port"])
		self.client = pymongo.MongoClient(login_string)

		# self.db = self.client["sonata_processed"]
		self.db = self.client["sonata"]
		self.batch_size = batch_size
		self.skip = 0 	#1241470
		self.sd = startdate
		self.ed = enddate
		self.users = users

		#uniques
		self.unique_transaction_types = []

	def get_unique_users(self):
		return self.users

	def __add_unique_transaction_types(self, results):
		for entry in results:
			if entry["TYPE"] not in self.unique_transaction_types:
				self.unique_transaction_types.append(entry["TYPE"])
		
	def get_unique_transaction_types(self):
		return self.unique_transaction_types

	def read(self):
		acc_trans = self.db["tscm_account_transaction"]
		results = acc_trans.aggregate([
			{"$skip": self.skip},
			{"$limit": self.batch_size},
			{
				"$addFields": {
					"months": [
						"",
						"Jan",
						"Feb",
						"Mar",
						"Apr",
						"May",
						"Jun",
						"Jul",
						"Aug",
						"Sep",
						"Oct",
						"Nov",
						"Dec"
					]
				}

			},
			{
				"$addFields": {
					"date": {
						"$dateFromParts": {
							"year": {
								"$toInt": {
									"$substr": [
										"$ACTR_FINANCIAL_ACCT_PERIOD",
										7,
										4
									]
								}
							},
							"month": {
								"$indexOfArray": [
									"$months",
									{
										"$substr": [
											"$ACTR_FINANCIAL_ACCT_PERIOD",
											0,
											3
										]
									}
								]
							},
							"day": {
								"$toInt": {
									"$substr": [
										"$ACTR_FINANCIAL_ACCT_PERIOD",
										4,
										2
									]
								}
							}
						}
					}
				}
			},
			{
				"$match": {
					"$and": [
						# { "date": { "$gt": datetime.datetime(2018, 7, 1)}},
						# { "date": { "$lt": datetime.datetime(2018, 8, 20)}}
						{ "date": { "$gte": datetime.datetime(self.sd[0], self.sd[1], self.sd[2])}},
						{ "date": { "$lte": datetime.datetime(self.ed[0], self.ed[1], self.ed[2])}},
						{ "ACTR_LAST_UPDATED_BY": { "$in": self.users}}
					]
				}
			},
			{
				"$lookup": {
					"from": "tscm_client",
					"localField": "ACTR_CLIENT_ID",
					"foreignField": "CLNT_ID",
					"as": "client"
				},
			},
			{"$unwind": "$client"},
			{
				"$lookup": {
					"from": "tscm_transaction_type",
					"localField": "ACTR_TRANSACTION_TYPE_ID",
					"foreignField": "TTYP_ID",
					"as": "type"
				},
			},
			{"$unwind": "$type"},
			{
				"$project": {
					"_id": 0,
					"DATE_TIME": "$ACTR_FINANCIAL_ACCT_PERIOD",
					"USER": "$ACTR_LAST_UPDATED_BY",
					# "NAME": {"$concat": ["$client.CLNT_SURNAME", ", ", "$client.CLNT_FORENAME"]},
					"TYPE": "$type.TTYP_DESCRIPTION",
				}
			}
		])
		results = list(results)
		self.skip += self.batch_size
		self.__add_unique_transaction_types(results)
		return results


# r = TransactionReader(5)

# results = r.read()
# for result in results:
# 	for k in result.keys():
# 		print("{}: {}".format(k, result[k]))
# 	print("")

# print("--------------------------------------------")
# results = r.read()
# for result in results:
# 	for k in result.keys():
# 		print("{}: {}".format(k, result[k]))
# 	print("")

# users = r.get_unique_users()
# for user in users:
# 	print(user)