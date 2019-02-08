# import requests
# from lxml import html


import argparse
import time
import datetime
import numpy as np
import pandas as pd
from poloniex import poloniex


from matplotlib.finance import candlestick2_ohlc
from matplotlib.pyplot import ion, show 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.lines as mlines
import datetime as datetime

import logging



class Ethbot:
    #sets an option for better viewing of dataframes in console
    pd.set_option('display.expand_frame_repr', False)
    
    key = "AA7AGVMO-B14TG914-VY6P5ALP-1U5JCDIC"
    secret = "9b0e054b47ad9547ee26a1b617ee6eaae604fdb1f21b5ab30f600332bb2609f47050dab364136c594fe1f3e970225e8c095325fdf05b27dbd583a68ece486e57"
    #candlestick graph period
    candle_period={'5 mins':300,'15 mins':900,'30 mins':1800,'2 hours':7200,'4 hours':14400,'1 day':86400}
    #time offsets
    offset = {'day':86400,"hour":3600,'2 days':172800,'4 days':345600,'week':604800,'30 days':2592000,'year ago':31536000}
    
    
    
    def __init__(self,k = key,s = secret,period='4 hours',startTime='30 days', endTime = 9999999999, pair = "BTC_ETH",debug = False):
    
        self.account_key = k
        self.account_secret = s
        self.data_interval = self.candle_period[period]
        self.currency = pair
        self.start = int(time.time())-self.offset[startTime]
        self.end = endTime
        self.historicalData = None
        self.debug = debug
        self.lastTick = None
        #create poloniex bot
        self.bot = poloniex(self.account_key,self.account_secret)
        
        if(self.debug is True):
            logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(message)s',
                    )
        
       
    def getHistoricalData(self, per = '4 hours' , startTime = '30 days'):
        
        
        offset = int(time.time())-self.offset[startTime]
        self.end = int(time.time())
        period = self.candle_period[per]
        
        #get chart data
        historicalData = self.bot.api_query("returnChartData",{"currencyPair":self.currency,"start":offset,"end":self.end,"period":period})
        #get just the cangle stik graph data. it is a list of dicts and make a data frame
        data = pd.DataFrame(historicalData['candleStick'])
        self.historicalData = data[["date","high",'low','open','close',"volume","quoteVolume","weightedAverage"]]
        
        return self.historicalData
        
        
    
    
    
    def getTicker(self):
        
        self.lastTick = self.bot.returnTicker(self.currency)
        # if attribute in ticker:
#             return ticker[attribute]
#         else:
        #print(ticker)
        #logging.debug('Got ticker data' +" "+"Last Price"+" "+self.lastTick['last'])
        #return self.lastTick 
         
        
    
    
    
    #######################################################
    ##             indicators                            ##
    #######################################################
    # Ease of Movement 
    def EMV(self,win): 
        dm = ((self.historicalData['high'] + self.historicalData['low'])/2) - ((self.historicalData['high'].shift(1) + self.historicalData['low'].shift(1))/2)
        br = (self.historicalData['volume'] / 100000000) / ((self.historicalData['high'] - self.historicalData['low']))
        emv = dm / br 
        emv_sma = pd.Series(emv.rolling(window=win).mean(), name = 'EMV') 
        self.historicalData = self.historicalData.join(emv_sma) 
        
    #Commodity Channel Index scaled by a factor of 1/100 to account for etherium's low price
    def CCIover10000(self,win): 
        TP = (self.historicalData['high'] + self.historicalData['low'] + self.historicalData['close']) / 3 
        CCI = pd.Series(((TP - TP.rolling(window = win).mean()) / (0.015 * TP.rolling(window = win).std()))/10000,
        name = 'CCI') 
        self.historicalData = self.historicalData.join(CCI) 
        
    #gets the the SMAs over 50,100,200 data point windows
    def getSMAs(self,windows):
        df = pd.DataFrame()
        
        for i in range(len(windows)):    
            sma = pd.Series(self.historicalData['close'].rolling(windows[i]).mean(),name='SMA '+str(windows[i]))
            df[sma.name] = sma
            
        return df
     
     
    #window is a single number that the SMA is calculated over
    #bands is a list of float that represent the +/- percent value of the bands to be plotted against the 
    # the sma. i.e if band = [0.025,0.05] then series that correspond to +/- 2.5%, and +/- 5% will be plotted
    #along with the sma       
    def getSMAbands(self,window,bands):
        sma = pd.Series(self.historicalData['close'].rolling(window).mean(),name='SMA '+str(window))
        df = pd.DataFrame(sma)
        
        for i in range(len(bands)):    
            top = pd.Series((sma + (sma*bands[i])),name='SMA + '+str(bands[i]))
            print(top)
            bottom = pd.Series((sma - (sma*bands[i])),name='SMA - '+str(bands[i]))
            df=df.join(top)
            df=df.join(bottom)
             
        
        
        #print(df)
        #df1 = df.iloc[:,:2]
        #print(len(df1.columns))
        return df
    
        
        
    # Exponentially-weighted Moving Average 
    def EMA(self,window): 
        
        ##EMA using pandas built in function
        EMA = pd.Series(pd.ewma(self.historicalData['close'], span = window, min_periods = window - 1), 
        name = 'EMA '+str(window))
        
        self.historicalData = self.historicalData.join(EMA)
       
        
        
    def DEMA(self,window):
        EMA = pd.Series(pd.ewma(self.historicalData['close'], span = window, min_periods = window - 1,adjust=False), 
        name = 'EWMA')
        EMAsquare = pd.Series(pd.ewma(EMA, span = window, min_periods = window - 1,adjust=True), 
        name = 'EWMAsquare')
        DEMA = pd.Series(2*EMA-EMAsquare,name='DEMA '+str(window))
        self.historicalData = self.historicalData.join(DEMA)
        print(self.historicalData)
         
         
        
         
    def MACD(self,longWindow=26,shortWindow=12,signalWindow=9):
        #get long window ema of close data (default 26 data points)
        emaLong = pd.Series(pd.ewma(self.historicalData['close'], span = longWindow, min_periods = longWindow - 1),name = 'emaLong')
        #get short window of close data (default 12 data points)
        emaShort = pd.Series(pd.ewma(self.historicalData['close'], span = shortWindow, min_periods = shortWindow - 1),name = 'emaShort')
        #the difference between emaLong and emaShort
        MACD = pd.Series(emaShort-emaLong,name='MACD')
        #the 9 period ema of the MACD line
        emaSignal = pd.Series(pd.ewma(MACD, span = signalWindow, min_periods = signalWindow - 1),name = 'emaSignal')
        #The difference bewteen MACd and 9 period signal
        MACDhist = pd.Series(MACD-emaSignal,name='MACDhist')
        self.historicalData = self.historicalData.join(MACD)
        self.historicalData = self.historicalData.join(MACDhist)
        print(self.historicalData)
     
     
    #######################################################
    ##             Graphing functions                    ##
    #######################################################
    
        #Graphs bands, unnecessary function    
    def graphBands(self,df,colours):
        #helper function for date labeling used in chart plotting function
        def mydate(x,pos):
            try:
                return xdate[int(x)]
            except IndexError:
                return ''
        
        #fig = plt.figure(figsize=(7,5))
        fig, ax = plt.subplots()
        xdate = [datetime.datetime.fromtimestamp(i) for i in self.historicalData['date'].values]
        lines=[]
        
        
        for i in xrange(len(df.columns)):
            
            plt.plot(df.iloc[:,i],colours[i])
            lines.append(mlines.Line2D([], [], color=colours[i], markersize=15, label=df.iloc[:,i].name))
            #!!!!!!!
        
        plt.plot(self.historicalData['close'],'0.75')
        lines.append(mlines.Line2D([], [], color='0.75', markersize=15, label='close'))
        plt.legend(handles=lines,loc=0)    
        plt.ylabel('SMAs ')
        plt.grid(True)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(7))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
        fig.autofmt_xdate()
        fig.tight_layout()    
        plt.show()    
        
    def plotChartsSeperate(self,names):
        
        #helper function for date labeling used in chart plotting function
        def mydate(x,pos):
            try:
                return xdate[int(x)]
            except IndexError:
                return ''
        
        fig = plt.figure(figsize=(7,5))
        xdate = [datetime.datetime.fromtimestamp(i) for i in self.historicalData['date'].values]
    
        for i in range(len(names)):
            ax = fig.add_subplot(len(names), 1, (i+1))
            plt.plot(self.historicalData[names[i]],'g',self.historicalData['close'],'0.75')
            plt.ylabel(names[i])
            plt.grid(True)
        
        ax.xaxis.set_major_locator(ticker.MaxNLocator(7))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
        fig.autofmt_xdate()
        fig.tight_layout()    
        plt.show()
        
       
        
    def plotChartsSameGUI(self,df=[],names=[]):
        
        colours = ['firebrick','darkturquoise','royalblue','darkkhaki','gold','r','g','b','m',]
        #helper function for date labeling used in chart plotting function
        def mydate(x,pos):
            try:
                return xdate[int(x)]
            except IndexError:
                return ''
        
        #fig = plt.figure(figsize=(7,5))
        fig, ax = plt.subplots()
        fig.suptitle('SMAs over Ethereum Price', fontsize=20)
        xdate = [datetime.datetime.fromtimestamp(i) for i in self.historicalData['date'].values]
        lines=[]
        if names != []:
            for i in range(len(names)):
            
                plt.plot(df[names[i]],colours[i])
                lines.append(mlines.Line2D([], [], color=colours[i], markersize=15, label=df[names[i]].name))
            
        
        plt.plot(self.historicalData['close'],'0.6')
        lines.append(mlines.Line2D([], [], color='0.6', markersize=15, label='close'))
        plt.legend(handles=lines,loc=0)    
        plt.ylabel('Price')
        plt.grid(True)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(7))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
        fig.autofmt_xdate()
        
        return fig
        
        
    def plotMACD(self):
        
        #helper function for date labeling used in chart plotting function
        def mydate(x,pos):
            try:
                return xdate[int(x)]
            except IndexError:
                return ''
        
        #fig = plt.figure(figsize=(7,5))
        fig, ax = plt.subplots()
        xdate = [datetime.datetime.fromtimestamp(i) for i in self.historicalData['date'].values]
        
        plt.plot(self.historicalData['MACD'].values,color='k',label='MACD')
        plt.plot(self.historicalData['MACDhist'].values,color='b',label='MACDhist')
        plt.ylabel('MACD and Histogram')
        plt.grid(True)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(7))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
        fig.autofmt_xdate()
        fig.tight_layout()
        plt.legend(loc=0)    
        plt.show() 
        
          
         

        
             
                   


