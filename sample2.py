import qstkutil.qsdateutil as du
import qstkutil.tsutil as tsu
import qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
from pylab import *
import pandas

#In this test, we find the correlation for energy stocks

symbols = ["CVX", "XOM", "BP", "PBR", "RDS-A", "$SPX"]

startday = dt.datetime(2006,1,1)
endday = dt.datetime(2010,12,31)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

dataobj = da.DataAccess("Yahoo")
voldata = dataobj.get_data(timestamps, symbols, "volume",verbose=True)
close = dataobj.get_data(timestamps, symbols, "close",verbose=True)
actualclose = dataobj.get_data(timestamps, symbols, "actual_close",verbose=True)

#plot actual close data for all stocks
plt.clf()
pricedata = actualclose.values #pulls 2D array out of pandas object
newtimestamps = actualclose.index
plt.plot(newtimestamps, pricedata)
plt.legend(symbols)
plt.ylabel("actualclose")
plt.xlabel("timestamps")
savefig("adjustedclose.pdf", format= 'pdf')


#Plot normalized price data for all stocks
normalizedata = pricedata/pricedata[0, :]
plt.clf()
plt.cla()
plt.plot(newtimestamps, normalizedata)
plt.legend(symbols)
plt.ylabel("Normalized Close")
plt.xlabel("Time")
savefig("normalizedclose.pdf",format = 'pdf') 



