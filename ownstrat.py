'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on March, 5, 2012

@author: Sourabh Bajaj
@contact: sourabhbajaj90@gmail.com
@summary: Event Profiler Tutorial
'''


import pandas 
from qstkutil import DataAccess as da
import numpy as np
import math
import copy
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu
import qstkstudy.EventProfiler as ep
import argparse
import csv
import qstkfeat.features as ft


"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""

# Get the data from the data store
storename = "Yahoo" # get data from our daily prices source
# Available field names: open, close, high, low, close, actual_close, volume
closefield = "close"
volumefield = "volume"
window = 10

parser = argparse.ArgumentParser(description = "Takes orders and outputs values file")

parser.add_argument("cash", type=float)
parser.add_argument("orders")

args = parser.parse_args()

def findEvents(symbols, startday,endday, marketSymbol,verbose=False):

	# Reading the Data for the list of Symbols.	
	timeofday=dt.timedelta(hours=16)
	timestamps = du.getNYSEdays(startday,endday,timeofday)
	dataobj = da.DataAccess('Yahoo')
	if verbose:
            print __name__ + " reading data"
	# Reading the Data
	close = dataobj.get_data(timestamps, symbols, closefield)
	
	# Completing the Data - Removing the NaN values from the Matrix
	close = (close.fillna(method='ffill')).fillna(method='backfill')
	
	#CLOSE_UNCHANGED!!!!
	close_unchanged = dataobj.get_data(timestamps, symbols, closefield)
	close_unchanged = (close.fillna(method='ffill')).fillna(method='backfill')
	
	# Calculating Daily Returns for the Market
	tsu.returnize0(close.values)
	SPYValues=close[marketSymbol]

	# Calculating the Returns of the Stock Relative to the Market 
	# So if a Stock went up 5% and the Market rised 3%. The the return relative to market is 2% 
	mktneutDM = close - close[marketSymbol]
	np_eventmat = copy.deepcopy(mktneutDM)
	for sym in symbols:
		for time in timestamps:
			np_eventmat[sym][time]=np.NAN

	if verbose:
            print __name__ + " finding events"

	# Generating the Event Matrix
	# Event described is : Market falls more than 3% plus the stock falls 5% more than the Market
	# Suppose : The market fell 3%, then the stock should fall more than 8% to mark the event.
	# And if the market falls 5%, then the stock should fall more than 10% to mark the event.
	with open (args.orders, "w") as outFile:
		writer  = csv.writer(outFile)
		for symbol in symbols:
		    for i in range(1,len(mktneutDM[symbol])):
			if SPYValues[i]<-0.03 and mktneutDM[symbol][i] < -0.05 :
				ft.featAroon(close_unchanged[symbol][i], bDown=False) 
		     		writer.writerow([timestamps[i].year,timestamps[i].month,timestamps[i].day, symbol, "Buy", 100])
				writer.writerow([timestamps[i+5].year,timestamps[i+5].month,timestamps[i+5].day, symbol, "Sell", 100]) 
			


#################################################
################ MAIN CODE ######################
#################################################


symbols = np.loadtxt('SP500port.csv',dtype='S10',comments='#', skiprows=1)
# You might get a message about some files being missing, don't worry about it.

#symbols =['BFRE','ATCS','RSERF','GDNEF','LAST','ATTUF','JBFCF','CYVA','SPF','XPO','EHECF','TEMO','AOLS','CSNT','REMI','GLRP','AIFLY','BEE','DJRT','CHSTF','AICAF']
startday = dt.datetime(2008,1,1)
endday = dt.datetime(2010,12,31)
findEvents(symbols,startday,endday,marketSymbol='SPY',verbose=True)


