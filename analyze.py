import argparse
import datetime as dt
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

import qstkutil.qsdateutil as du
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu



parser = argparse.ArgumentParser(description = "Takes values.csv and prints statistics")

parser.add_argument("values")
parser.add_argument("market_symbol")

args = parser.parse_args()




dailyFund = []#have to append SPY values to this also
dailySPY = []
timestamps = []
with open (args.values, "rU") as valuesFile:
	reader = csv.reader(valuesFile, "excel")
	for row in reader:
		dailyFund.append(float(row[3]))
		timestamps.append(dt.datetime(int(row[0]), int(row[1]), int(row[2]), 16))

dataobj = da.DataAccess('Yahoo')
close = dataobj.get_data(timestamps, [args.market_symbol], 'close')
close = (close.fillna(method = "ffill")).fillna(method = "backfill")

SPYvalues = close.values

#now we have the 3 lists/ndarray we need to finish computing the statistics and plot the graph(SPYvalues, fund_value, timestamps)

fundReturns = np.ndarray(shape=(len(dailyFund)), buffer=np.array(dailyFund))
fundReturns = fundReturns / fundReturns[0]
SPYReturns = SPYvalues /SPYvalues[0,:]
	
plt.clf()
plt.plot(timestamps, fundReturns)
plt.plot(timestamps, SPYReturns)

plt.legend(["Fund", "SPY"])
plt.ylabel('Normalized Return')
plt.xlabel('Date')
savefig('perf.pdf',format='pdf')

TotalRET = (dailyFund[len(dailyFund)-1] / (dailyFund[0]))
print ("Total Return: " + str(TotalRET))

tsu.returnize1(fundReturns)


print fundReturns
"""
tsu.getSharpeRatio(fundDaily, 0.0)
print ("Sharpe Ratio:")
"""
"""
CODE for QUIZ question

i=0
for time in timestamps:
	if ((time.year == 2011) and (time.month == 2) and (time.day == 18)):
		print dailyFund[i]
	i+=1
print dailyFund[i]
"""
