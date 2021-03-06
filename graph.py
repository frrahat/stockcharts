#!/usr/bin/env python
# Copyright (c) 2013-2014, Mohiuddin Rana(rana.ca@gmail.com)
# This software is for my research Project and under developement. If you are planning to use it please email me.
# The installation process may take a bit time. I am using ubuntu for everthing. May not work in windows system. 
# Please let me know if you would like to me add any new features for this software. 
import ystockquote
import time
import datetime
import math
import re
# from pylab import *
import numpy as np
# from termcolor import colored
from classes.html import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

"""
sample usage:
>>> import ystockquote
>>> print ystockquote.get_price('GOOG')
"""
_oil        = ['XEG.TO', 'SU.TO', 'CNQ.TO', 'CVE.TO','IMO.TO','CPG.TO', 'ECA.TO', 'HSE.TO', 'ARX.TO','TOU.TO','VET.TO','SVY.TO']
_gold       = ['XGD.TO','G.TO','ABX.TO','FNV.TO','GOLD','AEM.TO', 'RGLD', 'ELD.TO','AU', 'K.TO','NEM','AGI.TO']
_tech       = ['F','NOK','FB','BB.TO']
_lowrisk    = ['MFC.TO', 'XFN.TO']
_all        = ['XEG.TO']

#Common Variable 
data        = [] # This global variable is used to store all the data
today       =time.strftime("%Y-%m-%d")
fromDate    ="2016-07-01"
numberOfDays= 12 # numberOfDays we are trying to calculate the average high and low of the price
histrogramdata = [] 

def internet_on():
    try:
        urllib2.urlopen('http://www.yahoo.com', timeout=5)
        return True
    except urllib2.URLError as err: 
        return True


def filldata(stock_symbol):
# This function gets historical data and fill  Open, high, low,  last price and volume information in data[] variable.   
# Also adds 3 new column in header row: Average High, Average Low, Action 

    global data
   # Get historical data 
    data = ystockquote.get_historical_prices(stock_symbol,fromDate,today)
    """
    During the day time if we run this above query it does not work welll. 
    We need to insert the data manually Updating the list with todays Data
    """
    #Date,Open,High,Low,Close,Volume,Average High,Average Low,Action,WeekDay
    if (time.strftime("%d-%b-%y") not in data[1][0]):
        print('getting todays data')
        today_data= ystockquote.get_all(stock_symbol) #  This is retrive only today's price
        data.insert(1,[])
        data[1].append(time.strftime("%d-%b-%y"))
        data[1].append(today_data['today_open'].replace('N/A',data[2][1]))
        data[1].append(today_data['todays_high'].replace('N/A',data[2][2]))
        data[1].append(today_data['todays_low'].replace('N/A',data[2][3]))
        data[1].append(today_data['previous_close'].replace('N/A',data[2][4]))
        data[1].append(today_data['volume'].replace('"NMS"',data[2][5]))
        # last_trade_price=today_data['last_trade_price']
        # k1=last_trade_price.find('<b>')
        # k2=last_trade_price.find('</b>')
        # data[1].append(last_trade_price[k1+3:k2])
        
#Calculating Average High of the array average 
def averagehigh(dataseg):
    averagehigh=0
    for listitem in dataseg:
        if listitem[0] != "Date":
            averagehigh += float (listitem[2])
    return  "{0:10.3f}".format(float(averagehigh/len(dataseg)))

#Calculating Average Low of the array average 
def averagelow(dataseg):
    averagelow=0
    for listitem in dataseg:
        if listitem[0] != "Date":
            averagelow += float (listitem[3])
    return "{0:10.3f}".format(float(averagelow/len(dataseg)))
"""
Calculating last 10 days average high
Adding Bull vs Bear in graphCIBC R/EST 'FRAC
"""
def addavgHighandLow():
    # Start days is the first day
    global data
    start =1 # First row[0] is the header column 
    #Adding Extra Columns header in row header
    # Date,Open,High,Low,Close,Volume,Average High,Average Low,Action
    data[0].extend(["Average High", "Average Low", "Action"]) 
    n=len(data)
    while (start)<n:
        datseg = data[start:min((start+numberOfDays),n)]
        # print(data[start])
        data[start].append(averagehigh(datseg)) 
        data[start].append(averagelow(datseg)) 
        # data[start].append(averagelow(datseg))
        if float(data[start][3]) > float(data[start][6]):
            data[start].append("BULL")
        elif float(data[start][2]) < float(data[start][7]): 
            data[start].append("BEAR")  
        else:
            data[start].append("----")
        start +=1

def addWeekDays():
    global data
    data[0].append("Weekday")
    n=len(data)
    for i in range(1,n):
        weekday=datetime.datetime.strptime(data[i][0], '%d-%b-%y').strftime('%A')
        data[i].append(weekday)

def printData():
    global data
    
    print("-" * 120) 

    for row in data:
        n = len(row)          
        for i in range(n):
            item=row[i]
            print(item,end=" ")
            padding=10-len(str(item))
            if(padding>0 and i<n-1):
                print(" "*padding,end="")
        print()
         
# Drawing the plot
def drawPlot(ticker):
    global data
    #Date,Open,High,Low,Close,Volume,Average High,Average Low,Action,WeekDay
    array=np.array(data)[::-1]

    high = array[:-1,2].astype(float)
    low = array[:-1,3].astype(float)
    avghigh = array[:-1,6].astype(float)
    avglow = array[:-1,7].astype(float)
    closing = array[:-1,4].astype(float)
    volume = array[:-1,5].astype(float)
    daysopen = array[:-1,1].astype(float)
    marketvolume = volume*low
    x = [i for i in range(1,len(data))]  # value of X axis 

    

#Drawing the plot. 
    fig = plt.figure()
    ax1 = fig.add_axes([0.05, 0.05, 0.9, 0.9])  # left, bottom, width, height (range 0 to 1)
        
    # ax2 =  fig.add_axes([0.05,0.05,.9,.2]
    # g-- o : green cirlce,  r--o: Red circle, k--o: 
    ax1.plot(x, high,'g--o', x, low,'r-o', x,avghigh,'k-o', x, avglow,'k-o', x, closing, 'b--o', x, daysopen, 'c--o', linewidth=2.0)
    ax1.set_title(ticker)
    ax1.yaxis.tick_right()
    
    # ax1.set_yticklabels(np.arange(min(low)-1, max(high)+1, 0.05))
    ax1.set_xlim(0,1)
    ax1.set_ylim(min(low)-.01, max(high)+0.1)
    ax1.xaxis.set_major_locator(MultipleLocator(1))
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_major_locator(MultipleLocator(min(avglow)/300))
    ax1.yaxis.set_minor_locator(MultipleLocator(min(avglow)/100))
    ax1.grid(which='major', axis='x', linewidth=0.25, linestyle='-', color='0.75')
    ax1.grid(which='minor', axis='x', linewidth=0.75, linestyle='-', color='0.75')
    ax1.grid(which='major', axis='y', linewidth=0.40, linestyle='-', color='0.75')
    ax1.grid(which='minor', axis='y', linewidth=0.75, linestyle='-', color='0.75')
    
   # Adding the volume on The right side
    ax2 = ax1.twinx()
    ax2.plot(x, volume, 'y--o' )
    # Making the second figure for the plot
    plt.figure(2)
   #Sorting the result because it does not  work well without sorting. I need to test it more  
    sortedhigh =sorted(high, reverse=True)
    sortedlow = sorted (low, reverse = True)
    data_1 = np.vstack([sortedlow,sortedhigh]).T

    plt.hist(data_1,50, alpha=0.7, label = ['low', 'high'])
    plt.legend(loc = 'upper right')
    plt.show()

def main ():  
    # if (internet_on()==True):

    #     print "Parsing data from the net..."
    #     html1  = html("test")
    #     html1.getHeader("foo")

    #     filldata("MSFT")
    #     addavgHighandLow()
    #     printData()
    #     ticker="foo"
    #     drawPlot(data, ticker)
    # else: 
    #     print "No Internet Connection"
    
    filldata("GOOG")
    addavgHighandLow()
    addWeekDays()
    printData()
    drawPlot("foo")

if __name__ == "__main__":
    main() ## with if

