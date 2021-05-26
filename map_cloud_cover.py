import numpy as np
import matplotlib.pyplot as plt
import pygrib # import pygrib interface to grib_api
import cartopy.crs as ccrs
import imageio

# 0 == Surface level which is found in the fmi-opendata-rcrhirlam-surface-grib S3 bucket
# 10 == Surface level (10m) for winds which is found in the fmi-opendata-rcrhirlam-surface-grib S3 bucket
# 1000 and above are constant-pressure vertical levels (1000 being 1000Hpa), which are found in the fmi-opendata-rcrhirlam-pressure-grib S3 bucket
current_level = 0

grbs = pygrib.open("/data/grib/numerical-hirlam74-forecast-TotalCloudCover-20210524T000000Z.grb2")
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
	if grb.validDate.date() == date_valid.date() and grb.parameterName.lower() == 'total cloud cover' and grb.level == current_level:
		uwind.append(grb.values)
		datetimes.append(grb.validDate)
uwind = np.array(uwind)

wind_mag = uwind

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
				cs = plt.contourf(lons,lats,wind_mag[idx],np.linspace(0,8,8),cmap=plt.cm.jet,extend='both')
				ax.text(23,61.5, d.isoformat(timespec="seconds"), horizontalalignment='center', transform=ccrs.Geodetic(), size=42)
				filename = '/data/out/%s-%s.png' % (current_level, d.isoformat(timespec="seconds"))
				cb=plt.colorbar()
				cb.ax.tick_params(labelsize=40)
				plt.savefig(filename)
				plt.close()

				image = imageio.imread(filename)
				writer.append_data(image) 
				idx += 1