import csv
import datetime
import random

class Successess():
	def __init__(self):
		self.ss = {}

	def add_success(self, msisdn, visit_num):
		if msisdn not in self.ss.keys():
			self.ss[msisdn] = {}
		if visit_num not in self.ss[msisdn].keys():
			self.ss[msisdn][visit_num] = 0
		self.ss[msisdn][visit_num] += 1

	def add_success_with_count(self, msisdn, visit_num, count):
		if msisdn not in self.ss.keys():
			self.ss[msisdn] = {}
		if visit_num not in self.ss[msisdn].keys():
			self.ss[msisdn][visit_num] = 0
		self.ss[msisdn][visit_num] += count

	def length(self):
		count = 0
		for key in self.ss.keys():
			for key2 in self.ss[key].keys():
				count += 1
		return count

	def getMaxes(self):
		l1 = 0
		l2 = 0
		l3 = 0
		l4 = 0
		for key in self.ss.keys():
			for key2 in self.ss[key].keys():
				if self.ss[key][key2] > l4:
					l4 = self.ss[key][key2]
					if l4 > l3:
						l3,l4 = l4,l3
					if l3 > l2:
						l2,l3 = l3,l2
					if l2 > l1:
						l1,l2 = l2,l1

		print("l1: {}".format(l1))
		print("l2: {}".format(l2))
		print("l3: {}".format(l3))
		print("l4: {}".format(l4))

	def getOutput(self):
		new_list = []
		for key in self.ss.keys():
			for key2 in self.ss[key].keys():
				value = self.ss[key][key2]
				new_dict = {
					"success_count": value,
					"msisdn": key,
					"visit_num": key2
				}
				new_list.append(new_dict)
		return new_list

	def getOutput_sampler(self, samples):
		new_list = []
		count = 0
		for key in self.ss.keys():
			for key2 in self.ss[key].keys():
				if count in samples:
					value = self.ss[key][key2]
					new_dict = {
						"success_count": value,
						"msisdn": key,
						"visit_num": key2
					}
					new_list.append(new_dict)
				count += 1
		return new_list

	def getOutput_sampler_list(self, samples):
		new_list = []
		count = 0
		for key in self.ss.keys():
			for key2 in self.ss[key].keys():
				if count in samples:
					value = self.ss[key][key2]
					new_list.append((key, key2))
				count += 1
		return new_list

	def subset_action_range(self, v_min, v_max):
		new_ss = Successess()
		for key in self.ss.keys():
			for key2 in self.ss[key].keys():
				value = self.ss[key][key2]
				if value >= v_min and value <= v_max:
					new_ss.add_success_with_count(key, key2, value)
		return new_ss


ss = Successess()
success_words = [
	"success",
	"SUCCESS",
	"thank you"
]

ranges = [
	[1,2],
	[3,4],
	[5,8],
	[9,20]
]

with open("C:/Users/Ramsay/Documents/GitHub/data/query-impala-376379-non-null-0331.csv") as csv_file:
	csv_reader = csv.DictReader(csv_file, delimiter=",")
	# row_count = 0
	for row in csv_reader:
		msisdn = row["msisdn"]
		visit_num = row["visit_num"]
		# event_timestamp = row["event_timestamp"]
		event_page = row["event_page"]
		found = False
		if visit_num != "NA":
			for success_word in success_words:
				if success_word in event_page:
					ss.add_success(msisdn, visit_num)
					break


for r in ranges:
	new_ss = ss.subset_action_range(r[0], r[1])
	l = new_ss.length()
	print("{}-{}: {}".format(r[0], r[1], new_ss.length()))
	sample = random.sample(range(0,l), 100)
	sampled_list = new_ss.getOutput_sampler_list(sample)
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
	with open("C:/Users/Ramsay/Documents/GitHub/data/query-impala-376379-non-null-0331_sampler_actions_{}-{}.csv".format(r[0],r[1]), "w", newline="") as csv_file:
		dict_writer = csv.DictWriter(csv_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(outrows)
	
# output = ss.getOutput()

# keys = output[0].keys()
# with open("C:/Users/Ramsay/Documents/GitHub/data/query-impala-376379-non-null-0331_sampler_.csv", "w", newline="") as csv_file:
# 	dict_writer = csv.DictWriter(csv_file, keys)
# 	dict_writer.writeheader()
# 	dict_writer.writerows(output)
