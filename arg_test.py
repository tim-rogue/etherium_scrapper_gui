from ethbot import Ethbot
from infiniteTimer import InfiniteTimer
import select
import sys, termios

          





    
    
#create an ethbot object
ethbot = Ethbot(debug=True)
ethbot.getHistoricalData()
#set a thread to update the historical chart data frame every 15min
historicalTimer = InfiniteTimer(900,ethbot.getHistoricalData,[])
#set a thread to update the last data frame every 15min
lastPriceTimer = InfiniteTimer(5,ethbot.getTicker,[])
historicalTimer.start()
lastPriceTimer.start()



try:
    while True:
        
        #Checks to see if anything has been types into
        stuff = select.select([sys.stdin,],[],[],0.0)[0]
        
        if stuff:
            #this line flushes the stdin buffer
            #if this wasn't here the above IF condition would pass
            #in perpetuity
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            command = raw_input("type command:   ")
            print(command)
            if('print smas' in command):
                smas = ethbot.getSMAs([10,50,100])
                ethbot.plotChartsSame(['SMA 10','SMA 50','SMA 100'],['r','g','b'],smas)
                
            
            
        else:
            pass
        
        
        
        
        
except KeyboardInterrupt:
    historicalTimer.cancel()
    lastPriceTimer.cancel()
    print('Exiting Ethbot....')








##calculates sma's with windows length provided in the windows list
# windows=[30,60,120]
# names=['SMA 30','SMA 60','SMA 120']
# colours = colours=['g','b','r','0.75']
# ethbot.getSMAs(windows)
# ethbot.plotChartsSame(names,colours)

# ##calculates the 14 day ease of movement of histrical close data
# ##and joins it to the historical data data frame
# ethbot.EMV(14)
# ##calculates the commodity channel index of histrical close data
# ##and joins it to the historical data data frame. CCI is scalled by 1/10000 to make it visible over ETH_BTC
# ##close data
# ethbot.CCIover10000(100)
# print(ethbot.historicalData)
# ethbot.EWMA(200)
# ##shows graphs for all indexes whose names are in the names[] list
# names = ['CCI','EMV','EWMA']
# colours=['g','b','r','0.75']
# ethbot.plotChartsSeperate(names)


##############################################
## This block gets and plots MACD indicator ##
##############################################
# ethbot.MACD()
# ethbot.plotMACD()

# bands=[0.025,0.05,0.1]
# colours=['k','m','m','r','r','b','b']
# bands=ethbot.getSMAbands(100,bands)
# ethbot.graphBands(bands,colours)

# ethbot.DEMA(50)
# ethbot.DEMA(100)
# ethbot.getSMAs([50,100])
# ethbot.EMA(50)
# ethbot.EMA(100)
# ethbot.plotChartsSame(['DEMA 50','DEMA 100','EMA 50','EMA 100','SMA 50','SMA 100'],['m','m','g','g','b','b'])



###############################################################
# This block plots open, high, low close in a candstick graph #
###############################################################

# fig, ax = plt.subplots()
# candlestick2_ohlc(ax,df['open'].values,df['high'].values,df['low'].values,df['close'].values,width=0.6)
# 
# xdate = [datetime.datetime.fromtimestamp(i) for i in df['date'].values]
# 
# ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
# 
# def mydate(x,pos):
#     try:
#         return xdate[int(x)]
#     except IndexError:
#         return ''
# 
# ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
# 
# fig.autofmt_xdate()
# fig.tight_layout()
# 
# plt.show()


#{u'volume': 48.29840363, 
# u'quoteVolume': 1168.39611269, 
# u'high': 0.04149782, 
# u'low': 0.0413, 
# u'date': 1493238000, 
# u'close': 0.04135757, 
# u'weightedAverage': 0.04133735, 
# u'open': 0.04135798}

