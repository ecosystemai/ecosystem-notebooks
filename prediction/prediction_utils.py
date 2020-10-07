import datetime
import time
import copy
import concurrent.futures
from prediction.apis import worker_h2o
from prediction.apis import data_management_engine
from prediction.apis import prediction_engine

def frame_csv_file(auth, filename, prefix, description):
	filecsv = filename + ".csv"
	filehex = filename + ".hex"
	parsed = worker_h2o.file_to_frame(auth, filecsv, 1, "comma")
	user_frame = {}
	user_frame["timestamp_parsed"] = datetime.datetime.now().isoformat()
	user_frame["parser"] = "CSV"
	user_frame["import"] = parsed["import"]
	user_frame["parseSetup"] = parsed["parseSetup"]
	user_frame["destination_frame"] = filehex
	user_frame["file_name"] = filecsv
	user_frame["description"] = description
	user_frame["first_row_column_names"] = "1"
	user_frame["separator"] = "comma"
	user_frame["frame_id"] = prefix + filename
	user_frame["columnProperties"] = parsed["columnProperties"]

	result = prediction_engine.save_user_frame(auth, user_frame)
	frame = worker_h2o.featurestore_to_frame(auth, user_frame)


def _async_thread(auth, j_dc_doc, count, total):
		while True:
			try:
				data_management_engine.add_documents(auth, j_dc_doc, info=False)
				print("{}/{}".format(count, total))
				break
			except:
				pass
	

def async_upload(auth, dataframe, db_name, col_name):
	data = list(dataframe.T.to_dict().values())
	j_dc_doc = {
		"database": db_name,
		"collection": col_name,
		"document": {}
	}

	with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
		count = 0
		for d in data:
			count += 1
			# if count >= 1000:
			# 	break
			j_dc_doc["document"] = dict(d)
			d2 = copy.deepcopy(j_dc_doc)
			executor.submit(_async_thread, auth, d2, count, len(data))