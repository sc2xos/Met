#%%
import os
import numpy as np
import datetime as dt
import urllib.error
import urllib.request

from numpy.lib.shape_base import dstack
#%%
start_date = dt.datetime(2020, 1, 1, 0)    #初期時刻
end_date = dt.datetime(2020, 1, 10, 0)     #終了時刻
time_width = 6
#%%
def make_date(start_date, end_date, time_width):
	read_date = start_date
	date_array = []                 
	while(  read_date <= end_date ):
		date_array.append(read_date.strftime("%Y%m%d%H%M"))
		read_date = read_date + dt.timedelta(hours=time_width)
	return np.array(date_array)
test = make_date(start_date, end_date, time_width)
print(test)
date = test[0]
year = date[0:4]
month = date[4:6]
day =  date[6:8]
print(year, month, day)
#%%
def download_file(date, dst_path):
	year, month, day = date[0:4], date[4:6], date[6:8]
	url = "http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/{0}/{1}/{2}/Z__C_RJTD_{3}00_MSM_GPV_Rjp_Lsurf_FH00-15_grib2.bin".format(year, month, day, date)
	try:
		with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
			local_file.write(web_file.read())
	except urllib.error.URLError as e:
		print(e)
#%%
def main():
	for date in make_date(start_date, end_date, time_width):
		dst_path = "./{0}/{1}".format(date[0:4],date[4:6])
		os.makedirs(dst_path, exist_ok=True)
		download_file(date, dst_path)
#%%
if __name__ == '__main__':
	main()
#%%