import Tkinter as tk
from ethbot import Ethbot


class GUI_bot:
    
    def __init__(self, master):
        self.master = master
        self.lastTickText=tk.StringVar()
        #assign a master/root widget to a frame widget
        frame = tk.Frame(master)
        #call the pack method to make the frame visible
        frame.pack()
        #instantiate an ethbot object
        self.ethbot = Ethbot()
        #get historical chart data from the ethbot object
        self.getChart()
        #get Ticker data data from the ethbot object
        #self.getLastTick()
        #calculate the SMA of various windows from poloniex historical data
        #and plot them with matplotlib
        #self.plotSMAs()
        #create a label that holds the lastTickerText variable.
        # THis updates the lable anytime the lastTIckerText changes
        # self.tickerLabel = tk.Label(master, textvariable=self.lastTickText)
#         self.tickerLabel.pack(side=tk.TOP)
        #create quit button that calls the quit method when pressed
        self.quit_button = tk.Button(frame, text="QUIT", fg="red", command=frame.quit)
        #place the button as far left as possible within the frame
        self.quit_button.pack(side=tk.BOTTOM)
        #create a button that gets historical data from poloniex everytime the button is pressed
        # self.chartDataButton = tk.Button(frame, text="Get Chart Data", command=self.getChart)
#         self.chartDataButton.pack(side=LEFT)
        
        
    def getChart(self):
        self.ethbot.getHistoricalData()
        #print(self.ethbot.historicalData.iloc[[0]])
        #set up a repeated call of this function every 15 mins (900000 millisecs)
        self.master.after(900000,self.getChart)
        
    def getLastTick(self):
        #makes the ethbot object update its ticker variable with poloniex's API fuction getTicker
        self.ethbot.getTicker()
        self.lastTickText.set("Latest ETH_BTC Price: "+str(self.ethbot.lastTick['last']))
        #set up a repeated call of this function every 5 secs (5000 millisecs)
        print(str(self.ethbot.lastTick['last']))
        self.master.after(5000,self.getLastTick)
        
        
    def plotSMAs(self):
        smas = self.ethbot.getSMAs([10,50,100])
        self.ethbot.plotChartsSame(['SMA 10','SMA 50','SMA 100'],['r','g','b'],smas)
        self.master.after(900000,self.getLastTick)
        
        
        
    
        
                

root = tk.Tk()
gui = GUI_bot(root)
root.mainloop()
root.destroy()
        
        
        
