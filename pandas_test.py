import pandas as pd
#import pandas.io.data as web   # Package and modules for importing data; this code may change depending on pandas version
#from pandas_datareader import data, wb
import pandas_datareader.data as web
import datetime
import numpy as np
 
# #helper function that takes a 1D nd-array and a window size and 
# #computes the moving average across the data
# def simpleMovingAvg(data,window_size):
#     #print(data)
#     sum = 0.0
#     result = np.zeros(data.shape)
#     #the part of the moving average that is the up ramp
#     #i.e the part where the number of data points is less than the window
#     for i in range(0,window_size):
#         sum = sum + data[i]
#         #print(sum)
#         result[i] = sum/(i+1)
#         #print(result)
#     #the part of the moving average that has a full set of data point 
#     #the length of the window size    
#     for j in range(window_size,len(data)):
#         sum =  sum - data[i-window_size] + data[j] 
#         result[j] = sum/window_size
#         
#     return result 
 
dic = {'A': [1, 4, 1, 4], 'B': [9, 2, 5, 3], 'C': [0, 0, 5, 3]}
df = pd.DataFrame(dic)
print(df)
dic2={'A': [0, 0, 0, 0]}
df2 = pd.DataFrame(dic2)
df.update(df2[['A']]) 
print(df)
df3 = pd.DataFrame({'date':[0],"high":[0],'low':[0],'open':[0],'close':[0],"volume":[0],"quoteVolume":[0], "weightedAverage":[0]})
print(df3)
