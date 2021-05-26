import pickle, json, datetime, csv


def pickle_to_csv_and_json(fname):
	print("Loading %s" % ("/data/" + fname))
	data = pickle.load(open("/data/" + fname, 'rb'))


	all_keys = set()

	rows = []

	for d in data:
		for location_name in d:
			keys = d[location_name].keys()
			all_keys = (set(keys) - set(["times"])) | all_keys
			for ti in range(len(d[location_name]["times"])):
				row_data = {}
				row_data["location_name"] = location_name
				t = d[location_name]["times"][ti]
				row_data["timestamp"] = t.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
				for k in keys:
					if(k == "times"):
						continue
					val = d[location_name][k]["values"][ti]
					if(isinstance(val, datetime.datetime)):
						val = val.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
					row_data[k] = {"value": val, "unit": d[location_name][k]["unit"]}
				rows.append(row_data)

	#f = open("/data/transformed/" + fname.replace(".pickle", ".json"), 'w')
	#json.dump(rows,f)
	#f.close()


	with open("/data/transformed/" + fname.replace(".pickle", ".csv"), 'w') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=",", quotechar='"')
		headerRow = []
		headerRow.append("timestamp")
		headerRow.append("location_name")
		for k in sorted(all_keys):
			headerRow.append(k)
		csvwriter.writerow(headerRow)
		for r in rows:
			columns = []
			columns.append(r["timestamp"])
			columns.append(r["location_name"])
			for k in sorted(all_keys):
				columns.append(r[k]["value"])
			csvwriter.writerow(columns)

for year in range(2021,2022):
	pickle_to_csv_and_json("raw_fmi_data_weather-%s.pickle" % year)
	#pickle_to_csv_and_json("raw_fmi_data_weather_forecast_hirlam-%s.pickle" % year)
	pickle_to_csv_and_json("raw_fmi_data_wave-%s.pickle" % year)
	pickle_to_csv_and_json("raw_fmi_data_water_temp_level-%s.pickle" % year)
	
