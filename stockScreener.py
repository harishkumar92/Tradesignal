"""
a	 Ask
a2	 Average Daily Volume
a5	 Ask Size
b	 Bid
b2	 Ask (Real-time)
b3	 Bid (Real-time)
b4	 Book Value
b6	 Bid Size
c	 Change & Percent Change
c1	 Change
c3	 Commission
c6	 Change (Real-time)
c8	 After Hours Change (Real-time)
d	 Dividend/Share
d1	 Last Trade Date
d2	 Trade Date
e	 Earnings/Share
e1	 Error Indication (returned for symbol changed / invalid)
e7	 EPS Estimate Current Year
e8	 EPS Estimate Next Year
e9	 EPS Estimate Next Quarter
f6	 Float Shares
g	 Day's Low
h	 Day's High
j	 52-week Low
k	 52-week High
g1	 Holdings Gain Percent
g3	 Annualized Gain
g4	 Holdings Gain
g5	 Holdings Gain Percent (Real-time)
g6	 Holdings Gain (Real-time)
i	 More Info
i5	 Order Book (Real-time)
j1	 Market Capitalization
j3	 Market Cap (Real-time)
j4	 EBITDA
j5	 Change From 52-week Low
j6	 Percent Change From 52-week Low
k1	 Last Trade (Real-time) With Time
k2	 Change Percent (Real-time)
k3	 Last Trade Size
k4	 Change From 52-week High
k5	 Percebt Change From 52-week High
l	 Last Trade (With Time)
l1	 Last Trade (Price Only)
l2	 High Limit
l3	 Low Limit
m	 Day's Range
m2	 Day's Range (Real-time)
m3	 50-day Moving Average
m4	 200-day Moving Average
m5	 Change From 200-day Moving Average
m6	 Percent Change From 200-day Moving Average
m7	 Change From 50-day Moving Average
m8	 Percent Change From 50-day Moving Average
n	 Name	 n4	 Notes
o	 Open
p	 Previous Close
p1	 Price Paid
p2	 Change in Percent
p5	 Price/Sales
p6	 Price/Book
q	 Ex-Dividend Date
r	 P/E Ratio
r1	 Dividend Pay Date
r2	 P/E Ratio (Real-time)
r5	 PEG Ratio
r6	 Price/EPS Estimate Current Year
r7	 Price/EPS Estimate Next Year
 s	 Symbol	 s1	 Shares Owned
s7	 Short Ratio
t1	 Last Trade Time
t6	 Trade Links
t7	 Ticker Trend
t8	 1 yr Target Price
v	 Volume
v1	 Holdings Value
v7	 Holdings Value (Real-time)
 w	 52-week Range
w1	 Day's Value Change
w4	 Day's Value Change (Real-time)
 x	 Stock Exchange
y	 Dividend Yield"""

import pandas.io.data as web
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
import numpy as np
from pandas import Series, DataFrame
import urllib2
import urllib
import datetime
import csv

symbols = np.loadtxt('sp5002012.txt',dtype='S10',comments='#', skiprows=1)
orders = []

def analyzeStock(symbol):
     print symbol
     data = web.get_data_yahoo(symbol, '2012-01-01')
     analysis = pd.DataFrame(index = data.index)
     analysis['ADX'] = ta.ADX(data.High, data.Low, data.Close)
     analysis['RSI'] = ta.RSI(data.Close)

     last= len(analysis['ADX']) - 1
     if (analysis['ADX'][last]) > 10:#if there is a strong trend, use moving average crossovers + RSI
         analysis['SMA5'], analysis['SMA20'] = ta.SMA(data.Close,5), ta.MA(data.Close,20)
         analysis['PLUS_DI'] = ta.PLUS_DM(data.High, data.Low)
         analysis['MINUS_DI'] = ta.MINUS_DM(data.High, data.Low)
         ADX = analysis['ADX'][last]
         RSI = analysis['RSI'][last]
         SMA5 = analysis['SMA5'][last]
         SMA20 = analysis['SMA20'][last]
         DMIUP = analysis['PLUS_DI'][last]
         DMIDN = analysis['MINUS_DI'][last]

         if ((RSI < 35) and (SMA5>SMA20)):
            orders.append([symbol, 'BUY'])
         elif ((RSI > 65) and (SMA5 < SMA20)):
            orders.append([symbol, 'SELL'])
     elif (analysis['ADX'][last] < 10):
        analysis['BBANDUP'], analysis['BBANDDOWN'] = (ta.BBANDS(data.Close,20,2,1.5))[0], (ta.BBANDS(data.Close,20,2,1.5))[1]
        analysis['%K'], analysis['%D'] = ta.STOCHF(data.High, data.Low, data.Close)

        K = analysis['%K'][last]
        D = analysis['%D'][last]
        BANDDUP = analysis['BBANDUP'][last]
        BANDDOWN = analysis['BBANDDOWN'][last]
        CURR = data.Close[last]
        if ((CURR > BANDDUP) and (K > 80) and (D > 80) and (K<D)):
            orders.append([symbol,'SELL'])
        elif ((CURR < BANDDOWN) and (K<20) and (D<20) and (K>D)):
            orders.append([symbol,'BUY'])


for symbol in symbols:
    try:
        analyzeStock(symbol)
    except:
        print "Could not analyse:" + symbol



with open ("orders.csv", "w") as OutFile:
    writer = csv.writer(OutFile)
    for order in orders:
        writer.writerow(order)

