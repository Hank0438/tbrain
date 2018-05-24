#申購買回爬蟲
import requests
import numpy as np
import pandas as pd
import json

df = pd.DataFrame({"stkcd": [], "name": [], "ename": [], "qty": [], "cashinlieu": [], "minimum": []})
months = ['01','02','03','04']
days = [31,28,31,30]
for i in range(4):
    for j in range(days[i]):
        day = str(j+1)
        if(len(day)<=1): day = '0'+ day
        date = '2018' + months[i] + day
        url = 'http://www.yuantaetfs.com/api/Composition?date='+ date +'&fundid=1066'
        r = requests.get(url)
        df1 = pd.read_json(r.text)
        df1['date']=date
        df = pd.concat([df,df1], ignore_index=True)

fmt=['%c %8d %20s %c %5s %10d %4d']
np.savetxt('C:/Users/USER/Desktop/tbrain/broker_buy.txt', df.values, encoding='big5hkscs', fmt='%s')