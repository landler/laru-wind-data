import numpy as np
import matplotlib.pyplot as plt
import pygrib # import pygrib interface to grib_api
import cartopy.crs as ccrs
import imageio

# 10 == Surface level which is found in the fmi-opendata-rcrhirlam-surface-grib S3 bucket
# 1000 and above are constant-pressure vertical levels (1000 being 1000Hpa), which are found in the fmi-opendata-rcrhirlam-pressure-grib S3 bucket
current_level = 10  

grbs = pygrib.open("/data/grib/numerical-hirlam74-forecast-WindUMS-20210524T000000Z.grb2")
#for grb in grbs[:4]:
#    print(grb)

datetimes = []
#grbs.rewind() # rewind the iterator
from datetime import datetime
date_valid = datetime(2021,5,24,13)
uwind = []
for grb in grbs:
	print(grb.validDate)
	print(grb.parameterName)
	print(grb.level)
	if grb.validDate.date() == date_valid.date() and grb.parameterName == 'u-component of wind' and grb.level == current_level:
		uwind.append(grb.values)
		datetimes.append(grb.validDate)
uwind = np.array(uwind)


grbs = pygrib.open("/data/grib/numerical-hirlam74-forecast-WindVMS-20210524T000000Z.grb2")
#for grb in grbs[:4]:
#    print(grb)

vdatetimes = []
#grbs.rewind() # rewind the iterator
from datetime import datetime
date_valid = datetime(2021,5,24,13)
vwind = []
for grb in grbs:
	print(grb.validDate)
	print(grb.parameterName)
	print(grb.level)
	if grb.validDate.date() == date_valid.date() and grb.parameterName == 'v-component of wind' and grb.level == current_level:
		vwind.append(grb.values)
		vdatetimes.append(grb.validDate)
vwind = np.array(vwind)

usq = np.square(uwind)
vsq = np.square(vwind)
windtot = np.add(usq, vsq)
wind_mag = np.sqrt(windtot)



print(wind_mag.shape, wind_mag.min(), wind_mag.max())
lats, lons = grb.latlons()  # get the lats and lons for the grid.
print('min/max lat and lon',lats.min(), lats.max(), lons.min(), lons.max())




with imageio.get_writer('/data/out/%s.gif' % current_level, mode='I') as writer:
		idx = 0
		for d in datetimes:
				fig=plt.figure(figsize=(35,35))
				ax = plt.axes(projection=ccrs.PlateCarree())
				ax.coastlines(resolution='10m')
				ax.set_extent([22,27,58,62])
				cs = plt.contourf(lons,lats,wind_mag[idx],np.linspace(0,20,41),cmap=plt.cm.jet,extend='both')
				ax.text(23,61.5, d.isoformat(timespec="seconds"), horizontalalignment='center', transform=ccrs.Geodetic(), size=42)
				filename = '/data/out/%s-%s.png' % (current_level, d.isoformat(timespec="seconds"))
				cb=plt.colorbar()
				cb.ax.tick_params(labelsize=40)
				plt.savefig(filename)
				plt.close()

				image = imageio.imread(filename)
				writer.append_data(image) 
				idx += 1