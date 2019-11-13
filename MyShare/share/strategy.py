import pandas as pd
from pandas import DataFrame
import datetime
import os
import threading
import math
from time import ctime,sleep
import tushare as ts
from multiprocessing import Process,Lock

def runStrategy(ls,row):
    ls.ExecuteStategy(row)

class Strategy(object):
    """description of class"""
    def __init__(self,rdata):
        self.rdata = rdata
        self.liData = DataFrame()
        self.mutex = Lock()
        liThs = []
        length = len(rdata)
        
        for i in range(0,length,10):
            #测试
            if i+10 <= length:
                th = threading.Thread(name='%d'%i,target = runStrategy,args=(self,self.rdata[i:i+10]))
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
            symbol = row['symbol']

            if 'ST' in symbol or '退' in symbol or 'st' in symbol:
                continue
            path = './data/%s.csv'%code
            if not os.path.exists(path):
                continue
            rdf = pd.read_csv(path,encoding='gbk',dtype={'ts_code':object,'trade_date':object,'open':float,
                                                                     'high':float,'low':float,'close':float,'pre_close':float,
                                                                     'change':float,'pct_chg':float,'vol':float,'amount':float})
            if rdf is None or len(rdf) <20:
                continue
            rdf = self.nowadayDf(code,symbol,rdf)
            if self.IsCorporate(rdf):
                self.mutex.acquire()
                row['weight'] = Strategy.weight(rdf)
                self.liData = self.liData.append(row, ignore_index=True)
                self.mutex.release()

    def IsCorporate(self,df):
        return False

    @staticmethod
    def nowadayDf(code,symbol,rdf):
        #return rdf
        strtoday = datetime.datetime.now().strftime('%Y%m%d')
        if rdf.loc[0, 'trade_date'] != strtoday:
            
            tdf = ts.get_realtime_quotes(symbol)
            if tdf is not None:
                tradeday = datetime.datetime.strptime(tdf.ix[0, 'date'], '%Y-%m-%d')
                lastday = datetime.datetime.strptime(rdf.loc[0, 'trade_date'],'%Y%m%d')
                if tradeday > lastday:
                    open = float(tdf.ix[0, 'open'])
                    high = float(tdf.ix[0, 'high'])
                    low = float(tdf.ix[0, 'low'])
                    close = float(tdf.ix[0, 'price'])
                    pre_close = float(tdf.ix[0, 'pre_close'])
                    vol = float(tdf.ix[0, 'volume']) / 100
                    amount = float(tdf.ix[0, 'amount']) / 1000

                    rw = {'ts_code': [code], 'trade_date': [tradeday.strftime('%Y%m%d')], 'open': [open],'high': [high], 'low': [low], 
                          'close': [close], 'pre_close': [pre_close], 'change': [0.0],
                          'pct_chg': [(close - pre_close) / pre_close * 100], 'vol': [vol], 'amount': [amount]}
                    df_new = DataFrame(data=rw, index=None)
                        # columns = ['ts_code', 'trade_date', 'open', 'high', 'low', 'close',
                        #            'pre_close', 'change', 'pct_chg', 'vol', 'amount']
                        # old = rdf.loc[0:]

                    rdf = df_new.append(rdf, ignore_index=True,sort = True)
        return rdf

    @staticmethod
    def curDF(code,symbol):
        path = './data/%s.csv' % code
        if not os.path.exists(path):
            return None
        types = {'ts_code': object, 'trade_date': object, 'open': float,
                 'high': float, 'low': float, 'close': float, 'pre_close': float,
                 'change': float, 'pct_chg': float, 'vol': float, 'amount': float}
        rdf = pd.read_csv(path, encoding='gbk', dtype=types)
        if rdf is None or len(rdf) < 20:
            return rdf
        rdf = Strategy.nowadayDf(code, symbol, rdf)
        return rdf

    @staticmethod
    def isStrongArranged(rdata):
        """是否均线多头排列"""

        ema5 = Strategy.ema_n(rdata, 0, 5)
        ema13 = Strategy.ema_n(rdata, 0, 13)
        ema24 = Strategy.ema_n(rdata, 0, 24)
        ema54 = Strategy.ema_n(rdata, 0, 54)

        if ema5 == 0 or ema13 == 0 or ema24 == 0 or ema54 == 0:
            return False
        inc5 = (ema5 - ema13) / ema13
        inc13 = (ema13 - ema24) / ema24
        inc24 = (ema24 - ema54) / ema54

        if (inc5 > 0 and inc13 > 0) or (inc13 > 0 and inc24 > 0) or (inc5 > 0 and inc24 > 0):
            if (inc5 <= 0.065 and inc5 >= -0.065) and (inc13 <= 0.065 and inc13 >= -0.065) and (
                    inc24 <= 0.065 and inc24 >= -0.065):
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
    def weight(rdata):
        ema5 = Strategy.ma_n(rdata,0,5)
        ema13 = Strategy.ma_n(rdata,0,13)
        ema24 = Strategy.ma_n(rdata,0,24)
        ema54 = Strategy.ma_n(rdata,0,54)

        if ema5 == 0 or ema13 == 0 or ema24 == 0 or ema54 == 0:
            return 1
        sell5 = Strategy.sell_rate(ema5,rdata.loc[0,'close'],5)
        sell13 = Strategy.sell_rate(ema13,rdata.loc[0,'close'],13)
        sell24 = Strategy.sell_rate(ema24,rdata.loc[0,'close'],24)
        sell54 = Strategy.sell_rate(ema54,rdata.loc[0,'close'],54)
        return (1-sell5)*11+(1-sell13)*17+(1-sell24)*31+(1-sell54)*41


    @staticmethod
    def sell_rate(a,x,k):
        r = (x-a)/a
        return (1-math.exp(-k*r*r))
    
    @staticmethod
    def isAvlineBone(rdata):
        ema5 = Strategy.ema_n(rdata,0,5)
        ema13 = Strategy.ema_n(rdata,0,13)
        ema24 = Strategy.ema_n(rdata,0,24)
        ema54 = Strategy.ema_n(rdata,0,54)
        
        if ema5 == 0 or ema13 == 0 or ema24 == 0 or ema54 == 0:
            return False
        inc5 = (ema5-ema13)/ema13
        inc13 = (ema13-ema24)/ema24
        inc24 = (ema24-ema54)/ema54

        if (inc5 > 0 and inc13>0) or (inc13 > 0 and inc24 > 0) or (inc5 >0 and inc24 > 0):
            if (inc5 <= 0.0015 and inc5 >= -0.0015) and (inc13 <= 0.0015 and inc13 >= -0.0015) and (inc24 <= 0.004 and inc24 >= -0.004):
                return True
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

