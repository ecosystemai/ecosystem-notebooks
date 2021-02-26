import pymongo
import sys
import time

#Date enrichment needs to run on eff_date

def getFieldValues(field,collection):
#All the values of a specific field in a collection
	dollar_field = "$"+field
	field_group_pipeline = [
		{"$group":{"_id":None,"values":{"$push":dollar_field}}}
	]
	cursor_group_fields = db[collection].aggregate(field_group_pipeline)
	doc = cursor_group_fields.next()
	print(doc)
	listOfFields = doc["values"]
	return listOfFields

def enrich(mongoclient, destinations, db_name, proc_tx_data, proc_customer_data, cto_data, sample_tx_data_rollup, sample_tx_data_rollup_norm):
	client = pymongo.MongoClient(
		mongoclient
	)
	db = client[db_name]
	#Add ecosystem category to destinations
	db[proc_tx_data].create_index("destination")
	db[proc_tx_data].create_index("cust_no")
	with open(destinations, "r") as inputFile:
		for line in inputFile: 
			destination, code = line.split(",")
			db[proc_tx_data].update_many({"destination":destination[1:-1]},{"$set":{"MERCH_SIC_CDE":int(code[:-1])}})

	db[proc_tx_data].update_many({"MERCH_SIC_CDE":{"$exists":False}},{"$set":{"MERCH_SIC_CDE":999999}})
	db[proc_tx_data].create_index("MERCH_SIC_CDE")

	# Add budget categories and personality indicators to the data
	db["budgetCategoriesRefined"].create_index("ecosystem_coded")
	db["personalityCorpus"].create_index("ecosystem_code")
	enrich_pipeline = [ 
		{ 
			"$lookup":{ 
				"from":"budgetCategoriesRefined",
				"localField":"MERCH_SIC_CDE",
				"foreignField":"ecosystem_coded",
				"as":"subs"
			} 
		},
		{ 
			"$lookup":{ 
				"from":"codeToPersonality",
				"localField":"MERCH_SIC_CDE",
				"foreignField":"ecosystem_code",
				"as":"personalityCorpus"
			} 
		},
		{
			"$addFields":{
				"eco_base_code":{"$toString":{"$arrayElemAt":["$subs.eco_base_code",0]}},
				"spend_type":{"$toString":{"$arrayElemAt":["$subs.spend_type",0]}},
				"eco_category_code":{"$toString":{"$arrayElemAt":["$subs.eco_category_code",0]}},
				"eco_sub_code":{"$toString":{"$arrayElemAt":["$subs.eco_sub_code",0]}},
				"ecosystem_code":{"$toString":{"$arrayElemAt":["$subs.ecosystem_code",0]}},
				"year_eff_date_month":{"$concat":["$eff_date_year","$eff_date_month"]},
				"year_eff_date_week":{"$concat":["$eff_date_year","$eff_date_week_of_year"]}
			}
		},
		{
			"$unset":"subs"
		},
		{
			"$out":proc_tx_data
		}
	]
	db[proc_tx_data].aggregate(enrich_pipeline)
	db[proc_tx_data].create_index("cust_no")
	db[proc_tx_data].create_index("validTransaction")

	#Roll up the transactional data

	#Select fields for rollup
	rollUpFields = ["eff_date_week_of_year","eff_date_month","eff_date_week_and_day","eff_date_week_of_month","eff_date_public_holiday","personalityCorpus.trait_description","personalityCorpus.personality_description","trns_type","eff_date_day_of_week","eco_base_code","spend_type","eco_category_code","eco_sub_code","ecosystem_code"]

	#Create indices
	for i in rollUpFields:
		db[proc_tx_data].create_index(i)

	#Reset rollup table

	db[sample_tx_data_rollup].drop()

	#Rollup the transactional data
	total_pipeline = [{ 
						"$group":{ 
							"_id":"$cust_no",
							"spendTotal":{"$sum":"$trns_amt"},
							"frequencyTotal":{"$sum":1}
						} 
					},
					{
						"$merge":{
							"into": sample_tx_data_rollup,
							"on": "_id",
							"whenMatched": "merge",
							"whenNotMatched": "insert"
						} 
					}]
	db[proc_tx_data].aggregate(total_pipeline)
	for i in rollUpFields:
		listOfValues = db[proc_tx_data].distinct(i)
		for j in listOfValues:
			spendFieldName = str(j)+"spend"+"Total"
			frequnecyFieldName = str(j)+"frequency"+"Total"
			rollup_pipeline = [
							{"$match":{i:j}},
							{ 
								"$group":{ 
									"_id":"$cust_no",
									spendFieldName:{"$sum":"$trns_amt"},
									frequnecyFieldName:{"$sum":1}
								} 
							}, 
							{
								"$merge":{
									"into": sample_tx_data_rollup,
									"on": "_id",
									"whenMatched": "merge",
									"whenNotMatched": "insert" 
								} 
							}
			]
			db[proc_tx_data].aggregate(rollup_pipeline)

	#normalise the rolled up transactional data
	fields_pipeline = [
		{"$project":{"arrayofkeyvalue":{"$objectToArray":"$$ROOT"}}},
		{"$unwind":"$arrayofkeyvalue"},
		{"$group":{"_id":None,"allkeys":{"$addToSet":"$arrayofkeyvalue.k"}}}
	]
	cursor = db[sample_tx_data_rollup].aggregate(fields_pipeline)
	doc = cursor.next()
	listOfFields = doc['allkeys']
	if '_id' in listOfFields: 
		listOfFields.remove('_id')
	    
	normalise_project = {"$project":{}}
	for i in listOfFields:
		if i == "spendTotal":
			normalise_project["$project"][i[:-5]] = "$spendTotal"
		elif i == "frequencyTotal":
			normalise_project["$project"][i[:-5]] = "$frequencyTotal"
		elif i[0:5] == "spend":
			normalise_project["$project"][i[:-5]] = {"$divide":["$"+i,"$spendTotal"]}
		else:
			normalise_project["$project"][i[:-5]] = {"$divide":["$"+i,"$frequencyTotal"]}

	normalise_pipeline = [normalise_project, {"$out":sample_tx_data_rollup_norm}]

	db[sample_tx_data_rollup].aggregate(normalise_pipeline)

	#add personality types
	personalityType_pipeline = [
		{
			"$addFields":{
				"personalityArray":[
					{"personality":"Extrovert","deriv":{"$divide":[{"$subtract":["$ExtrovertFrequency",0.3608]},0.3608]}},
					{"personality":"Introvert","deriv":{"$divide":[{"$subtract":["$IntrovertFrequency",0.5883]},0.5883]}},
					{"personality":"Industrious","deriv":{"$divide":[{"$subtract":["$IndustriousFrequency",0.46792]},0.46792]}},
					{"personality":"Experiential","deriv":{"$divide":[{"$subtract":["$ExperientialFrequency",0.08867]},0.08867]}},
					{"personality":"Enthusiastic","deriv":{"$divide":[{"$subtract":["$EnthusiasticFrequency",0.04602]},0.04602]}},
					{"personality":"Intentional","deriv":{"$divide":[{"$subtract":["$IntentionalFrequency",0.4001]},0.4001]}}
				]
			}
	    },
	    {
			"$addFields":{
				"personalityTypeArray":{
					"$filter": {
						"input": "$personalityArray",
						"as": "item",
						"cond": { "$eq": ["$$item.deriv", { "$max": "$personalityArray.deriv" }]}
					}
				}
			}
		},
		{
			"$addFields":{
				"personalityType":{"$slice":["$personalityTypeArray.personality",1]},
				"CUST_NO": "$_id"
			}
		},
		{"$unwind":"$personalityType"},
		{"$unset":"personalityArray"},
		{"$unset":"personalityTypeArray"},
		{"$out":sample_tx_data_rollup_norm}
	]
	db[sample_tx_data_rollup_norm].aggregate(personalityType_pipeline)

	join_cto_pipeline = [
		{
			"$lookup":{
				"from":cto_data,
				"localField":"CUST_NO",
				"foreignField":"CUST_NO",
				"as":"subs"
			}
		},
		{
			"$addFields":{"CTO":"$subs.CTO"}
		},
		{"$unwind":"$CTO"},
		{"$unset":"subs"},
		{"$out":proc_customer_data}
	]
	db[proc_customer_data].aggregate(join_cto_pipeline)
	cust_norm_pipeline = [
		{
			"$addFields":{
				"MTD_CR_INT_PD_AMTs":{"$cond":[{"$gt":["$CTO",0]},{"$divide":["$MTD_CR_INT_PD_AMT",{"$divide":["$CTO",100]}]},-1]},
				"MTD_DR_INT_RCV_AMTs":{"$cond":[{"$gt":["$CTO",0]},{"$divide":["$MTD_DR_INT_RCV_AMT",{"$divide":["$CTO",50]}]},-1]},
				"CUST_TOT_DR_BALs":{"$cond":[{"$gt":["$CTO",0]},{"$divide":["$CUST_TOT_DR_BAL",{"$divide":["$CTO",1]}]},-1]},
				"CUST_TOT_CR_BALs":{"$cond":[{"$gt":["$CTO",0]},{"$divide":["$CUST_TOT_CR_BAL",{"$divide":["$CTO",1]}]},-1]}
			}
		},
		{"$out":proc_customer_data}
	]
	db[proc_customer_data].aggregate(cust_norm_pipeline)

	# merge_rollup_customer_pipeline = [
	# 	{
	# 		"$merge":{
	# 			"into": proc_customer_data,
	# 			"on": "CUST_NO",
	# 			"whenMatched": "merge",
	# 			"whenNotMatched": "insert" 
	# 		} 
	# 	}
	# ]
	# db[sample_tx_data_rollup_norm].aggregate(merge_rollup_customer_pipeline)
	merge_rollup_customer_pipeline = [
		{
			"$lookup":{
				"from":sample_tx_data_rollup_norm,
				"localField":"CUST_NO",
				"foreignField":"CUST_NO",
				"as":"subs"
			}
		},
		{
			"$addFields":{
				"Nonefrequency":"$subs.Nonefrequency",
				"ElectronicPaymentsspend":"$subs.ElectronicPaymentsspend",
				"Cashspend":"$subs.Cashspend",
				"Otherspend":"$subs.Otherspend",
				"CardPurchasesspend":"$subs.CardPurchasesspend",
				"Cashfrequency":"$subs.Cashfrequency",
				"Nonespend":"$subs.Nonespend",
				"ElectronicPaymentsfrequency":"$subs.ElectronicPaymentsfrequency",
				"Transfersspend":"$subs.Transfersspend",
				"frequency":"$subs.frequency",
				"CardPurchasesfrequency":"$subs.CardPurchasesfrequency",
				"Otherfrequency":"$subs.Otherfrequency",
				"Transfersfrequency":"$subs.Transfersfrequency",
				"Prepaid_Buyfrequency":"$subs.Prepaid_Buyfrequency",
				"Prepaid_Buyspend":"$subs.Prepaid_Buyspend",
				"DebitOrdersfrequency":"$subs.DebitOrdersfrequency",
				"personalityType":"$subs.personalityType",
				"DebitOrdersspend":"$subs.DebitOrdersspend",
				"spend":"$subs.spend",
				"Feesspend":"$subs.Feesspend",
				"Feesfrequency":"$subs.Feesfrequency"
			}
		},
		{"$unwind":"$Nonefrequency"},
		{"$unwind":"$ElectronicPaymentsspend"},
		{"$unwind":"$Cashspend"},
		{"$unwind":"$Otherspend"},
		{"$unwind":"$CardPurchasesspend"},
		{"$unwind":"$Cashfrequency"},
		{"$unwind":"$Nonespend"},
		{"$unwind":"$ElectronicPaymentsfrequency"},
		{"$unwind":"$Transfersspend"},
		{"$unwind":"$frequency"},
		{"$unwind":"$CardPurchasesfrequency"},
		{"$unwind":"$Otherfrequency"},
		{"$unwind":"$Transfersfrequency"},
		{"$unwind":"$Prepaid_Buyfrequency"},
		{"$unwind":"$Prepaid_Buyspend"},
		{"$unwind":"$DebitOrdersfrequency"},
		{"$unwind":"$personalityType"},
		{"$unwind":"$DebitOrdersspend"},
		{"$unwind":"$spend"},
		{"$unwind":"$Feesspend"},
		{"$unwind":"$Feesfrequency"},
		{"$unset":"subs"},
		{"$out":proc_customer_data}
	]
	db[proc_customer_data].aggregate(merge_rollup_customer_pipeline)

def main():
	# mongoclient = "mongodb://ecosystem_user:EcoEco321@localhost:54445"

	# destinations = "listOfDestinations.txt"

	# db_name = "fnb"
	# proc_tx_data = "transactions_upload"
	# proc_customer_data = "customers_upload"
	# cto_data = "CTO_upload"

	# sample_tx_data_rollup = "transactions_rollup_test"
	# sample_tx_data_rollup_norm = "transactions_rollup_normalise_test"

	mongoclient = sys.argv[1]

	destinations = sys.argv[2]

	db_name = sys.argv[3]
	proc_tx_data = sys.argv[4]
	proc_customer_data = sys.argv[5]
	cto_data = sys.argv[6]

	sample_tx_data_rollup = sys.argv[7]
	sample_tx_data_rollup_norm = sys.argv[8]

	enrich(mongoclient, destinations, db_name, proc_tx_data, proc_customer_data, cto_data, sample_tx_data_rollup, sample_tx_data_rollup_norm)
main()

# python3 /data/enrich_for_runtime.py "mongodb://ecosystem_user:EcoEco321@localhost:54445" "/data/listOfDestinations.txt" "fnb" "transactions_upload" "customers_upload" "CTO_upload" "transactions_rollup_test" "transactions_rollup_normalise_test"