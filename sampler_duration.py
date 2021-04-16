import csv
import datetime
import random

class Durations():
	def __init__(self):
		self.mvn = {}

	def addTime(self, time, msisdn, visit_num):
		if msisdn not in self.mvn:
			self.mvn[msisdn] = {}
		if visit_num not in self.mvn[msisdn]:
			self.mvn[msisdn][visit_num] = Duration(msisdn, visit_num)
		self.mvn[msisdn][visit_num].addTime(time)

	def length(self):
		count = 0
		for key in self.mvn.keys():
			for key2 in self.mvn[key].keys():
				count += 1
		return count

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

	def getOutput_sampler(self, samples):
		new_list = []
		count = 0
		for key in self.mvn.keys():
			for key2 in self.mvn[key].keys():
				if count in samples:
					value = self.mvn[key][key2]
					new_dict = {}
					dur = self.mvn[msisdn][visit_num]
					new_dict["msisdn"] = msisdn
					new_dict["visit_num"] = visit_num
					new_dict["datetime_min"] = dur.min
					new_dict["datetime_max"] = dur.max
					new_dict["duration"] = dur.getDuration()
					new_list.append(new_dict)
				count += 1
		return new_list

	def getOutput_sampler_list(self, samples):
		new_list = []
		count = 0
		for key in self.mvn.keys():
			for key2 in self.mvn[key].keys():
				if count in samples:
					new_list.append((key, key2))
				count += 1
		return new_list

	def subset_action_range(self, v_min, v_max):
		new_ds = Durations()
		for key in self.mvn.keys():
			for key2 in self.mvn[key].keys():
				value = self.mvn[key][key2].getDuration()
				if value >= v_min and value <= v_max:
					new_ds.addTime(value, key, key2)
		return new_ds

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
				return
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

success_words = [
	"success",
	"SUCCESS",
	"thank you"
]

ranges = [
	[15,69],
	[70,139],
	[140,499],
	[500,40000]
]

ds = Durations()

with open("C:/Users/Ramsay/Documents/GitHub/data/query-impala-376379-non-null-0331.csv") as csv_file:
	csv_reader = csv.DictReader(csv_file, delimiter=",")
	for row in csv_reader:
		msisdn = row["msisdn"]
		visit_num = row["visit_num"]
		event_timestamp = row["event_timestamp"]
		event_page = row["event_page"]

		found = False
		if visit_num != "NA":
			for success_word in success_words:
				if success_word in event_page:
					ds.addTime(event_timestamp, msisdn, visit_num)
					break


for r in ranges:
	new_ds = ds.subset_action_range(r[0], r[1])
	l = new_ds.length()
	print("{}-{}: {}".format(r[0], r[1], new_ds.length()))
	sample = random.sample(range(0,l), 100)
	sampled_list = new_ds.getOutput_sampler_list(sample)
	print(sampled_list)
	outrows = []
	with open("C:/Users/Ramsay/Documents/GitHub/data/query-impala-376379-non-null-0331.csv") as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=",")
		# row_count = 0
		for row in csv_reader:
			msisdn = row["msisdn"]
			visit_num = row["visit_num"]
			# event_timestamp = row["event_timestamp"]
			# event_page = row["event_page"]
			if (msisdn, visit_num) in sampled_list:
				outrows.append(row)
	keys = outrows[0].keys()
	with open("C:/Users/Ramsay/Documents/GitHub/data/query-impala-376379-non-null-0331_sampler_duration_{}-{}.csv".format(r[0],r[1]), "w", newline="") as csv_file:
		dict_writer = csv.DictWriter(csv_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(outrows)
	
# output = ss.getOutput()

# keys = output[0].keys()
# with open("C:/Users/Ramsay/Documents/GitHub/data/query-impala-376379-non-null-0331_sampler_.csv", "w", newline="") as csv_file:
# 	dict_writer = csv.DictWriter(csv_file, keys)
# 	dict_writer.writeheader()
# 	dict_writer.writerows(output)
