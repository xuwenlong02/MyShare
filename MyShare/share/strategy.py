import pandas as pd
from pandas import DataFrame
import datetime
import os
import threading
import math
from time import ctime,sleep
import tushare as ts

def runStrategy(ls,row):
    ls.ExecuteStategy(row)

class Strategy(object):
    """description of class"""
    def __init__(self,rdata):
        self.rdata = rdata
        self.liData = DataFrame()
        liThs = []
        length = len(rdata)
        for i in range(0,length,20):
            #测试
            if i+20 <= length:
                th = threading.Thread(name='%d'%i,target = runStrategy,args=(self,self.rdata[i:i+20]))
            else:
                th = threading.Thread(name='%d'%i,target = runStrategy,args=(self,self.rdata[i:-1]))

            liThs.append(th)
            th.start()  
            

        for th in liThs:
            th.join(30)

    def resultList(self):
        return self.liData

    def ExecuteStategy(self,piece):
        for index,row in piece.iterrows():
            code = row['ts_code']
            path = './data/%s.csv'%code
            if not os.path.exists(path):
                continue
            rdf = pd.read_csv(path,encoding='gbk',dtype={'ts_code':object,'trade_date':object,'open':float,
                                                                     'high':float,'low':float,'close':float,'pre_close':float,
                                                                     'change':float,'pct_chg':float,'vol':float,'amount':float})
            if rdf is None or len(rdf) <20:
                continue
            strtoday = datetime.datetime.now().strftime('%Y%m%d')
            if rdf.loc[0, 'trade_date'] != strtoday:
                symbol = row['symbol']
                tdf = ts.get_realtime_quotes(symbol)
                if tdf is not None:
                    strdate = tdf.ix[0, 'date']
                    if datetime.datetime.strptime(strdate, '%Y-%m-%d') == datetime.datetime.strptime(strtoday,
                                                                                                     '%Y%m%d'):
                        open = float(tdf.ix[0, 'open'])
                        high = float(tdf.ix[0, 'high'])
                        low = float(tdf.ix[0, 'low'])
                        close = float(tdf.ix[0, 'price'])
                        pre_close = float(tdf.ix[0, 'pre_close'])
                        vol = float(tdf.ix[0, 'volume']) / 100
                        amount = float(tdf.ix[0, 'amount']) / 1000

                        rw = {'ts_code': [code], 'trade_date': [datetime.datetime.now().strftime('%Y%m%d')],
                              'open': [open],
                              'high': [high], 'low': [low], 'close': [close], 'pre_close': [pre_close], 'change': [0.0],
                              'pct_chg': [(close - pre_close) / pre_close * 100], 'vol': [vol], 'amount': [amount]}
                        df_new = DataFrame(data=rw, index=None)
                        # columns = ['ts_code', 'trade_date', 'open', 'high', 'low', 'close',
                        #            'pre_close', 'change', 'pct_chg', 'vol', 'amount']
                        # old = rdf.loc[0:]

                        rdf = df_new.append(rdf, ignore_index=True,sort = True)
            if self.IsCorporate(rdf):
                self.liData = self.liData.append(row, ignore_index=True)

    def IsCorporate(self,df):
        return False

    @staticmethod
    def isStrongArranged(rdata):
        """是否均线多头排列"""
        ema5 = Strategy.ma_n(rdata,0,5)
        ema10 = Strategy.ma_n(rdata,0,10)
        ema24 = Strategy.ma_n(rdata,0,24)
        ema54 = Strategy.ma_n(rdata,0,54)

        if ema5 == 0 or ema10 == 0 or ema24 == 0:
            return False
        if not Strategy.trendUpward(rdata):
            return False
        if Strategy.greaterThan(ema5,ema54) and Strategy.greaterThan(ema10,ema54):
            return True
        return False
    
    def greaterThan(v1,v2):
        mid = (v1+v2)/2
        diff = (v1-v2)/mid 
        if diff>= -0.009 and diff < 0.18:
            return True
        return False

    def equalTo(v1,v2):
        mid = (v1+v2)/2
        diff = (v1-v2)/mid 
        if diff>= -0.009 and diff <= 0.009:
            return True
        return False
    
    @staticmethod
    def isAvlineBone(rdata):
        ema5 = Strategy.ema_n(rdata,0,5)
        ema10 = Strategy.ema_n(rdata,0,10)
        ema24 = Strategy.ema_n(rdata,0,24)
        
        if ema5 == 0 or ema10 == 0 or ema24 == 0:
            return False

        if Strategy.trendUpward(rdata):
            if Strategy.equalTo(ema5,ema10) and Strategy.equalTo(ema10,ema24):
                return True
        return False

    @staticmethod
    def trendUpward(rdata):
        ema5_0 = Strategy.ma_n(rdata,0,5)
        ema5_1 = Strategy.ma_n(rdata,1,5)
        #ema5_2 = Strategy.ma_n(rdata,2, 5)
        ema10_0 = Strategy.ma_n(rdata, 0, 10)
        ema10_1 = Strategy.ma_n(rdata, 1, 10)
        #ema10_2 = Strategy.ma_n(rdata, 2, 10)
        if ema5_0 == 0 or ema5_1 == 0 or ema10_0 == 0 or ema10_1 == 0:
            return False
        if (ema5_0 - ema10_0) >= (ema5_1-ema10_1):
            return True
        # vct5 = ema5_0-ema5_1
        # vct10 = ema10_0-ema10_1
        # cos = (1+vct5*vct10)/(math.sqrt((1+vct5*vct5))*math.sqrt(1+vct10*vct10))
        # if cos >0 and cos < 0.73:
        #     return True
        return False

    @staticmethod
    def ema_n(rdata,k,n):
        """计算N日移动均线"""
        if rdata is None:
            return 0
        if len(rdata) < n+k:
            return 0
        if len(rdata) == k+n:
            return rdata.loc[k,'close']
        return (2*rdata.loc[k,'close']+(n-1)*Strategy.ema_n(rdata,k+1,n))/(n+1)

    @staticmethod
    def ema_pre_n(rdata,y0,k,n):
        """计算N日移动均线"""
        if rdata is None:
            return 0
        if len(rdata) < n+k:
            return 0
        if len(rdata) == k+n:
            return rdata.loc[k,'close']
        return (2*rdata.loc[k,'close']+(n-1)*y0)/(n+1)

    @staticmethod
    def ma_n(rdata,k,n):
        """计算N日均线"""
        if rdata is None:
            return 0
        if len(rdata)<k+n:
            return 0
        total = 0
        for i in range(k,k+n,1):
            total = total + rdata.loc[i,'close']
        return total/n

    @staticmethod
    def mv_n(rdata,k,n):
        if rdata is None:
            return 0
        if len(rdata)<k+n:
            return 0
        total = 0
        for i in range(k,k+n,1):
            total = total + rdata.loc[i,'vol']
        return total/n

    @staticmethod
    def av_slope(rdata,n):
        if rdata is None or len(rdata) == 0:
            return -100
        ma1 = Strategy.ma_n(rdata,0,n)
        ma2 = Strategy.ma_n(rdata,1,n)
        try:
            return (ma1-ma2)/rdata.loc[1,'close']
        except:
            print(rdata)
            return -100

    @staticmethod
    def is_vol_right(rdata,k):
        if (rdata.loc[k, 'close'] > rdata.loc[k+1,'close'] and rdata.loc[k, 'vol'] >= rdata.loc[k+1,'vol']) or (
                    rdata.loc[k, 'close'] <= rdata.loc[k+1,'close'] and rdata.loc[k, 'vol'] <= rdata.loc[k+1,'vol']):
            return True
        return False

