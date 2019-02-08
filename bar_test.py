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
import matplotlib.pyplot as plt


from ethbot import Ethbot
import numpy as np
import pandas as pd

def mydate(x,pos):
            try:
                return xdate[int(x)]
            except IndexError:
                return ''
                
ethbot = Ethbot()
ethbot.getHistoricalData()
ethbot.getTicker()

fig = plt.figure()
ax_vol = fig.add_subplot(2,1,2)
xdate = [datetime.datetime.fromtimestamp(i) for i in ethbot.historicalData['date'].values]
ax_vol.bar(xdate,ethbot.historicalData['volume'])
ax_vol.grid(True)
ax_vol.xaxis.set_major_locator(ticker.MaxNLocator(7))
ax_vol.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
fig.autofmt_xdate()
plt.hold(True)
plt.ion()
plt.show()
