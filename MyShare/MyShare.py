import tushare as ts
import os
import numpy as np
import pandas as pd
from pandas import DataFrame as df
import os
import threading

from PyQt5.QtGui import QPen,QColor
from PyQt5.QtCore import Qt

#pen = QPen(QColor(223,223,223),1,Qt.SolidLine)


#code=input('股票代码:')
#start=input('开始日期，格式YYYY-MM-DD:')
#end=input('结束日期，格式YYYY-MM-DD:')
#os.makedirs(r'%s/k线数据'%code)
#os.makedirs(r'%s/复权数据'%code)

#print("%.2f%%"%34.5)

#ts.get_today_all().to_csv("sz000001.csv")
#ts.get_index().to_csv("a.csv")
#df = ts.get_realtime_quotes('000581')
#print(df)
#dt = ts.get_stock_basics().to_csv("./data/stocks.csv",encoding='gbk')
#stocks = pd.read_csv('./data/stocks.csv',encoding='gbk')
#print(stocks.ix[0])
#print(type(stocks.ix[0,'name']))
#print(type(stocks.ix[0,'code']))
#print(type(stocks.ix[0,'industry']))
#print("%s[%06d]\n%s"%(stocks.ix[0,'name'],stocks.ix[0,'code'],stocks.ix[0,'industry']))
#print(type(stocks))
#data = pd.DataFrame(stocks,columns=['code','name','industry'])
#print(data)
#print(type(np.array(dt).tolist()))
#list =dt #np.array(dt).tolist()
#print(dt.ix[0])
#print(dt.index[0]+dt.ix[0,'name']+'\n'+dt.ix[0,'industry'])



#d = ts.get_hist_data('600848',start='2019-09-30', ktype='5') #获取5分钟k线数据
#pd.set_option("display.max_columns",500)
#rdata = ts.get_realtime_quotes('002504')
pro = ts.pro_api('604a0f99c257e0a0f3ae4ed6291a99e986f482be8083e561f09622ad')
#df = pro.daily(ts_code='002504.SH',start_date='20191008',end_date='20191019')
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,industry,market')
print(data)
df = pro.daily(ts_code='002504.SH',trade_date='20191018')
print(df)
def func():
     for i in range(0,200,9):
            listCode = []
            for j in range(i,i+9,1):
                if j >= 200:
                    break
                print("index = %d\n"%(j))
                listCode.append(j)
            t = threading.Thread(target = run_stock,args =listCode,daemon = True,)
            t.start()

def run_stock(*list):
    pass
#func()
