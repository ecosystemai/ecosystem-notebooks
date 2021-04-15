import csv
import datetime
# visit_num
# event_timestamp

# 2021-00-01 10:16:47

class Durations():
	def __init__(self):
		self.mvn = {}

	def addTime(self, time, msisdn, visit_num):
		if msisdn not in self.mvn:
			self.mvn[msisdn] = {}
		if visit_num not in self.mvn[msisdn]:
			self.mvn[msisdn][visit_num] = Duration(msisdn, visit_num)
		self.mvn[msisdn][visit_num].addTime(time)

	def getOutput(self):
		new_list = []
		for msisdn in self.mvn.keys():
			for visit_num in self.mvn[msisdn].keys():
				new_dict = {}
				dur = self.mvn[msisdn][visit_num]
				new_dict["msisdn"] = msisdn
				new_dict["visit_num"] = visit_num
				new_dict["datetime_min"] = dur.min
				new_dict["datetime_max"] = dur.max
				new_dict["duration"] = dur.getDuration()
				new_list.append(new_dict)
		return new_list

class Duration():
	def __init__(self, msisdn, visit_num):
		self.msisdn = msisdn
		self.visit_num = visit_num
		self.min = None
		self.max = None

	def addTime(self, time):
		dt = None
		try:
			format = "%Y-%m-%d %H:%M:%S"
			dt = datetime.datetime.strptime(time, format)
		except:
			try:
				format = "%Y-%m-%d %H:%M:%S:%f"
				dt = datetime.datetime.strptime(time, format)
			except:
				pass
		if self.min == None:
			self.min = dt
		if self.max == None:
			self.max = dt
		if dt < self.min:
			self.min = dt
		if dt > self.max:
			self.max = dt

	def getDuration(self):
		return (self.max - self.min).total_seconds()


ds = Durations()

with open("C:/Users/Ramsay/Documents/GitHub/data/query-impala-376379-non-null-0331.csv") as csv_file:
	csv_reader = csv.DictReader(csv_file, delimiter=",")
	# row_count = 0
	for row in csv_reader:
		msisdn = row["msisdn"]
		visit_num = row["visit_num"]
		event_timestamp = row["event_timestamp"]
		ds.addTime(event_timestamp, msisdn, visit_num)
		# row_count += 1
		# if row_count >= 10:
		# 	break

output = ds.getOutput()
print(len(output))


keys = output[0].keys()
with open("C:/Users/Ramsay/Documents/GitHub/data/query-impala-376379-non-null-0331_duration_format.csv", "w", newline="") as csv_file:
	dict_writer = csv.DictWriter(csv_file, keys)
	dict_writer.writeheader()
	dict_writer.writerows(output)
