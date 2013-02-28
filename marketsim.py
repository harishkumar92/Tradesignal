import argparse
import datetime as dt
import pandas as pd
import csv

import qstkutil.qsdateutil as du
import qstkutil.DataAccess as da

def updateFund(fund_value, current_cash, curr_ownership, symbols, close, datetime):
	x=0
	for symbol in symbols:
		if (curr_ownership.has_key(symbol)):
			x += (curr_ownership[symbol] * 	close[symbol][datetime])

	fund_value.append([datetime, (current_cash + x)])

parser = argparse.ArgumentParser(description = "Takes orders and outputs values file")

parser.add_argument("cash", type=float)
parser.add_argument("orders")
parser.add_argument("values")

args = parser.parse_args()


#Set up 2D Array to store orders(convert orders.csv to pandas datamatrix)
orders = [] 

with open (args.orders, "rU") as inputFile:
	with open (args.values, "w") as outFile:
		reader = csv.reader(inputFile, "excel")
		writer = csv.writer(outFile)

		for row in reader:
			orders.append([dt.datetime(int(row[0]), int(row[1]), int(row[2]), 16), row[3],row[4],row[5]])



#get timestamps for trading days

timeofday = dt.timedelta(hours=16)
startday = min(orders)[0]
endday = max(orders)[0]
timestamps = du.getNYSEdays(startday, endday,timeofday)

#get unique symbols
symbols = []

for order in orders:
	symbols.append(order[1])

symbols = list(set(symbols))

#get data
closefield = 'close'
dataobj = da.DataAccess('Yahoo')
close = dataobj.get_data(timestamps, symbols, 'close')
close = (close.fillna(method = "ffill")).fillna(method = "backfill")



current_cash = args.cash
cash=[]#2d array of timestamps and cash values on that particular datetime stamp
curr_ownership={}
fund_value=[]
for datetime in timestamps:
	for order in orders:
		if datetime == order[0]:
			if "Buy" == order[2]:
				current_cash = current_cash - (close[order[1]][datetime]* int(order[3]))
				cash.append([datetime, current_cash])
				if curr_ownership.has_key(order[1]):
					curr_ownership[order[1]] = curr_ownership[order[1]] + int(order[3])
				else:
					curr_ownership[order[1]] = int(order[3])
			else:
				current_cash = current_cash + (close[order[1]][datetime]* int(order[3]))
				cash.append([datetime, current_cash])
				if curr_ownership.has_key(order[1]):
					curr_ownership[order[1]] = curr_ownership[order[1]] - int(order[3])
				else:
					curr_ownership[order[1]] = 0 - int(order[3])
		else:
			cash.append([datetime, current_cash])
	updateFund(fund_value, current_cash, curr_ownership, symbols, close, datetime)




with open (args.values, "w") as outFile:
	writer = csv.writer(outFile)
	for value in fund_value:
		date = dt.date(value[0].year, value[0].month, value[0].day)
		writer.writerow([value[0].year, value[0].month, value[0].day, value[1]])
	


