#from owslib.wfs import WebFeatureService
import json, datetime, pickle, time
import signal
from fmiopendata.wfs import download_stored_query

#snd = download_stored_query("fmi::observations::weather::sounding::multipointcoverage")
#wav = fmi::observations::wave::multipointcoverage
# Water temp and current forecast fmi::forecast::hbm::point::multipointcoverage
# Salinity and water temperature observations fmi::observations::ctd::multipointcoverage
# Sea level and temperature observations fmi::observations::mareograph::instant::multipointcoverage
datasets = [
			["weather", "fmi::observations::weather::multipointcoverage"],
			##["sounding", "fmi::observations::weather::sounding::multipointcoverage"],
			#["wave", "fmi::observations::wave::multipointcoverage"],
			##["water_temp_salinity", "fmi::observations::ctd::multipointcoverage"],
			#["water_temp_level", "fmi::observations::mareograph::instant::multipointcoverage"],
			##["water_temp_current_forecast", "fmi::forecast::hbm::point::multipointcoverage"],
			#["weather_forecast_hirlam", "fmi::forecast::hirlam::surface::obsstations::multipointcoverage"]
			]


def timeout_handler(signum, frame):
	print("Request timed out!")
	raise Exception("timeout")

signal.signal(signal.SIGALRM, timeout_handler)

for dataset in datasets:
	#start_time = datetime.datetime(2014,6,14,0,0)
	start_time = datetime.datetime(2020,1,1,0,0)
	total_end_time = datetime.datetime.utcnow() #datetime.datetime(2021,5,25,0,0)
	hour_step = 2

	datas = []

	time_started = time.time()
	fetch_count = 0

	while start_time < total_end_time:
		# Retrieve the latest hour of data from a bounding box
		end_time = start_time + datetime.timedelta(hours=hour_step)

		# Convert times to properly formatted strings
		start_time_s = start_time.isoformat(timespec="seconds") + "Z"
		# -> 2020-07-07T12:00:00Z
		end_time_s = end_time.isoformat(timespec="seconds") + "Z"
		# -> 2020-07-07T13:00:00Z

		args_this_time = ["bbox=22,59.4,27,60.5",
                                  "starttime=" + start_time_s,
                                  "endtime=" + end_time_s,
                                  "timeseries=True"]

		if("forecast" not in dataset[0] and not dataset[0] == "weather"):
			args_this_time.append("timestep=" + str(1000 * 60 * 10))
		print(args_this_time)
		signal.alarm(10)
		try:
			obs = download_stored_query(dataset[1],
		                            args=args_this_time)
		except Exception as exc:
			print("Retrying fetch")
			continue
		signal.alarm(0)

		#print(sorted(obs.data.keys()))
		#latest_tstep = max(obs.data.keys())
		#print(sorted(obs.data[latest_tstep].keys()))
		#print(obs.data)
		print(len(obs.data))
		if(dataset[0] == "weather"):
			datas.append(obs.data)
		elif(dataset[0] == "sounding"):
			datas.append(obs.soundings)
		else:
			datas.append(obs.data)

		start_time = start_time + datetime.timedelta(hours=hour_step)
		fetch_count += 1
		print("%s: At time %s. Avg time of %s per hour of data." % (dataset[0], start_time, (time.time()-time_started) / (fetch_count*hour_step)))

		if(start_time.day==1 and start_time.month==1 and start_time.hour==0):
			pickle.dump(datas, open("/data/raw_fmi_data_%s-%s.pickle" % (dataset[0], start_time.year-1), "wb"))
			datas = []

	pickle.dump(datas, open("/data/raw_fmi_data_%s-%s.pickle" % (dataset[0], total_end_time.year), 'wb'))
