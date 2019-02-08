import Tkinter as tk
import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import datetime as datetime
import matplotlib.lines as mlines
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

from ethbot import Ethbot
import numpy as np
import pandas as pd


LARGE_FONT = ("verdana",12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)
style.use("ggplot")



def popupmsg(msg):

    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()        

    


class PoloniexApp(tk.Tk):
    
    def __init__(self, *args,**kwargs):
        
        
        #initializes the parent class Tk
        #always has to happen with child classes
        tk.Tk.__init__(self,*args,**kwargs)
        tk.Tk.wm_title(self,"Ethbot Trader")
        #initalizes the frame widget of tkinter
        container = tk.Frame(self)
        # container.pack(side="top",fill="both",expand=True)
        container.pack(fill="both",expand=True)
        #container.grid(row=0,column=1)
        # container.grid_rowconfigure(0,weight=1)
#         container.grid_columnconfigure(0,weight=1)
        
        ##start defining the menu bar we will have in the app
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        #adds a label to the file menu and a command for this label
        filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported just yet!"))
        #add a line to file menu
        filemenu.add_separator()
        #adds a quit label and functionality
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        ##indicator menu
        # mainI = tk.Menu(menubar, tearoff=1)
#         mainI.add_command ( label="None",command=lambda: addMiddleIndicator('none'))
#         mainI.add_separator()
#         mainI.add_command ( label="SMA",command=lambda: addMiddleIndicator('sma'))
#         mainI.add_command ( label="EMA",command=lambda: addMiddleIndicator('ema'))
#         menubar.add_cascade(label = "Main Graph Indicator", menu = mainI)

        
        
        #adds the menubar to the app
        tk.Tk.config(self, menu=menubar)
        
        
        self.frames={}
        
        for F in (StartPage,PoloniexPage):
            frame=F(container,self)
            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky="nsew")
            
        self.show_frame(StartPage)
        
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
        
    
        
class StartPage(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Ethbot Trading\nApplication",font=LARGE_FONT)
        label.grid(row=0,column=0)
        button1 = ttk.Button(self,text="Agree", command=lambda:controller.show_frame(PoloniexPage))
        button1.grid(row=1,column=50)
        button2 = ttk.Button(self,text="Disagree", command=quit)
        button2.grid(row=2,column=100)
        
        
        
        
class PoloniexPage(tk.Frame):
    
    def __init__(self,parent,controller):
        #instantiate an ethbot object
        self.ethbot = Ethbot(startTime = 'year ago',period='2 hours')
        self.ethbot.getHistoricalData()
        self.ethbot.getTicker()
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Graph Page",font=LARGE_FONT)
        label.grid(row=0,column=0)
        button1 = ttk.Button(self,text="Go back Home ", command=lambda:controller.show_frame(StartPage))
        button1.grid(row=0,column=1)
        
        
        
        self.sma_entry_label = tk.Label(self, text="Enter SMA lengths seperated by commas")
        self.sma_entry_label.grid(row=0,column = 5)
        self.sma_entry = tk.Entry(self, bd =5)
        self.sma_entry.grid(row=0,column = 6)
        
        # self.button_left = tk.Button(self,text="Plot SMAs", command=lambda:self.plotSMAs())
#         self.button_left.grid(row=1,column = 6)
#         
#         
#         
#         #the modes to be used by radio buttons
#         periodModes = [("5 mins", "5 mins"),("15 mins", "15 mins"),("30 mins", "30 mins"),
#                        ("2 hours", "2 hours"),("4 hours", "4 hours"),("1 day", "1 day")]
#         offsetModes = [('day', 'day'),("hour", "hour"),('2 days', '2 days'),
#                        ('4 days', '4 days'),('week', 'week'),("30 days", "30 days"),('year ago', 'year ago')]
#         #setting up the two string variables used by the radio buttons for selecting
#         #graph period and time frame              
#         self.periodVar = tk.StringVar()
#         self.periodVar.set('4 hours') # initialize
#         self.offsetVar = tk.StringVar()
#         self.offsetVar.set('30 days') # initialize
        
        # #creating the radio buttons
#         i = 5
#         for text, mode in periodModes:
#             b = tk.Radiobutton(self, text=text,
#                             variable=self.periodVar, value=mode)
#             b.grid(row = i ,column = 0)
#             i+=1
#             
#         i = 5    
#         for text, mode in offsetModes:
#             b = tk.Radiobutton(self, text=text,
#                             variable=self.offsetVar, value=mode)
#             b.grid(row = i ,column = 2)
#             i+=1
#             
#         self.button_change = tk.Button(self,text="Change Graph Period and Time Frame", command=lambda:self.plotPriceVol(self.periodVar.get(),self.offsetVar.get(),True))
#         self.button_change.grid(row = 7 ,column = 1)
        
        
        #self.fig = Figure()
        #self.plotPriceVol(self.periodVar.get(),self.offsetVar.get(),False)
        
        
       #  #add graph to canvas and pack into Tkinter widget
#         self.canvas = FigureCanvasTkAgg(self.fig,self)
#         self.canvas.show()
#         self.canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
#         
#         ## Code form the tutorial but doesn't show toolbar
#         self.toolbar = NavigationToolbar2TkAgg(self.canvas,self)
#         self.toolbar.update()
#         self.canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

    # def plotSMAs(self):
#         
#         #get the values from the entry field and split them at commas
#         #if entry field isn't empty
#         colours = ['firebrick','lightseagreen','darkorchid','gold','coral','r','g','b']
#         if self.sma_entry.get():
#             print("entry field wasn't empty")
#             #if there are SMa already plotted then clear them
#             if len(self.lines) > 1:
#                 self.plotPriceVol(self.periodVar.get(),self.offsetVar.get(),True)
#             windows = self.sma_entry.get().split(',')
#             #turn all the strings in the windows list into integers
#             windows = map(int,windows)
#             #get the SMA over the specified windows
#             smas = self.ethbot.getSMAs(windows)
#             #get the names of the columns in the sma data frame for the figure legend
#             names = smas.columns.values.tolist()
#             for j in range(len(names)):
#                 
#                 self.ax_price.plot(self.xdate,smas[names[j]], color = colours[j]) 
#                 self.lines.append(mlines.Line2D([], [], color = colours[j], markersize=15, label=smas[names[j]].name))
#             self.ax_price.legend(handles=self.lines,loc=0)
#             self.canvas.draw()
#         else:
#             self.plotPriceVol(self.periodVar.get(),self.offsetVar.get(),True)
#             self.ax_price.legend(handles=self.lines,loc=0)
#             self.canvas.draw()
#         
#     def plotPriceVol(self, period = '4 hours', startTime = '30 days', redraw = False):
#         
#         #if we are redrawing price data clear the existing data
#         if redraw == True:
#             #clear axes
#             self.ax_price.cla()
#             #clear figure
#             self.fig.clf()
#         temp_frame = self.ethbot.getHistoricalData(period,startTime)
#         self.xdate = [datetime.datetime.fromtimestamp(i) for i in temp_frame['date'].values]
#         self.ax_price = self.fig.add_subplot(2,1,1)
#         self.lines = []
#         self.line, = self.ax_price.plot(self.xdate,temp_frame['close'],'0.6')
#         self.lines.append(mlines.Line2D([], [], color='0.6', markersize=15, label='close'))
#         self.ax_price.legend(handles=self.lines,loc=0)    
#         self.ax_price.grid(True)
#         self.ax_vol = self.fig.add_subplot(2,1,2,sharex=self.ax_price)
#         self.ax_vol.bar(self.xdate,temp_frame['volume'],0.05)
#         self.ax_vol.grid(True)
#         self.ax_vol.xaxis.set_major_locator(ticker.MaxNLocator(10))
#         self.ax_vol.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
#         self.fig.autofmt_xdate()
#         
#         #if we are redrawing pricea data redraw the canvas
#         if redraw == True:
#             self.canvas.draw()
        
         
        
    
app = PoloniexApp()
app.geometry("1280x720")
app.mainloop()
    
    
    
    
    
    
    