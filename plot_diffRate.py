import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

names = ['stock_number','date','stock_name','open','high','low','close','volume']
dtype = {'stock_number':np.str, 'date':np.int32, 'open':np.float16,'high':np.float16,'low':np.float16,'close':np.float16,'volume':np.int32}

#dataset
tetfp = pd.read_csv('C:/Users/USER/Desktop/tbrain/dataset/tetfp.txt', encoding='big5hkscs',  sep='\s+', names=names, dtype=dtype, low_memory=False)
tetfp_2018 = tetfp[tetfp.date > 20180000]
tsharep = pd.read_csv('C:/Users/USER/Desktop/tbrain/dataset/tsharep.txt', encoding='big5hkscs', sep='\s+', names=names, dtype=dtype, low_memory=False)
tsharep_2018 = tsharep[tsharep.date > 20180000]
weight_0050 = pd.read_csv('C:/Users/USER/Desktop/tbrain/dataset/0050_2018s1.txt', encoding='big5hkscs', sep='\s+', names=['stock_number', 'stock_name', 'stock_rate'], dtype={'stock_number':np.str})

def diffRateGen(data):
    diffRate = [0.0]
    for i in range(len(data)):
        if(i != 0):
            if(data[i-1]==0): 
                diffRate.append(0)
            else: 
                diffRate.append((data[i]-data[i-1])/data[i-1])
    return diffRate

def closeGen(stock_number, dataset):
    close = dataset[dataset.stock_number==stock_number].close.values
    #possiblely shorter close_array
    if(len(close)!=75):
            close = np.concatenate([close, np.zeros(75-len(close))])
    return close
    
def weightETF():
    weighted_data = np.zeros(75)
    weighted_diffRate = np.zeros(75)
    for i in weight_0050.values:
        stock_number = i[0]
        weight = i[2]
        close = closeGen(stock_number, tsharep_2018)
        diffRate = diffRateGen(close)     
        weighted_data += np.multiply(diffRate,weight)
    return weighted_data

#blue
weighted_etf = weightETF()
#red
etf = tetfp_2018[tetfp_2018.stock_number=='0050'].close.values
etf_diffRate = diffRateGen(etf)

def plot_and_compare(weighted_etf, etf):
    date = np.arange(75)
    plt.plot(date, weighted_etf, color='blue')
    plt.plot(date, etf_diffRate, color='red')
    plt.xlabel("date") 
    plt.ylabel("price") 
    plt.title("weight_0050 V.S. 0050") 
    plt.show() 

plot_and_compare(weighted_etf, etf)