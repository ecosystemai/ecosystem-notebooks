import csv

def similar_event_timeline(values, prefix_field, datetime_field):
	injected_end = "injected_end_datetime"
	for i in range(len(values)-1):
		a = values[i]
		b = values[i+1]
		if a[prefix_field] == b[prefix_field]:
			a[injected_end] = b[datetime_field]
		else:
			a[injected_end] = a[datetime_field]
	values[-1][injected_end] = values[-1][datetime_field]
	return values

values = []
with open("C:/Users/Ramsay/Documents/GitHub/data/amcd_test_data2.csv", mode="r") as csv_file:
	csv_reader = csv.DictReader(csv_file)
	for value in csv_reader:
		values.append(dict(value))

values = sorted(values, key = lambda i: i["start"])	

tl_values = similar_event_timeline(values, "task", "start")

for tl_value in tl_values:
	print(tl_value)