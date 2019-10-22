import pandas as pd
from pandas import DataFrame
import datetime
import os
import threading
from time import ctime,sleep

def runStrategy(ls,row):
    ls.ExecuteStategy(row)

class Strategy(object):
    """description of class"""
    def __init__(self,rdata):
        self.rdata = rdata
        self.liData = DataFrame()
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
            path = './data/%s.csv'%code
            if not os.path.exists(path):
                continue
            df = pd.read_csv(path,encoding='gbk',dtype={'ts_code':object,'trade_date':object,'open':float,
                                                                     'high':float,'low':float,'close':float,'pre_close':float,
                                                                     'change':float,'pct_chg':float,'vol':float,'amount':float})
            if df is None or len(df) == 0:
                continue
            if self.IsCorporate(df):
                self.liData = self.liData.append(row, ignore_index=True)

    def IsCorporate(self,df):
        return False

    @staticmethod
    def isStrongArranged(rdata):
        """是否均线多头排列"""
        ema5 = Strategy.ema_n(rdata,0,5)
        ema10 = Strategy.ema_n(rdata,0,10)
        ema24 = Strategy.ema_n(rdata,0,24)
        #ema54 = Strategy.ema_n(rdata,0,54)

        if ema5 == 0 or ema10 == 0 or ema24 == 0:
            return False
        if not Strategy.trendUpward(rdata):
            return False
        if Strategy.greaterThan(ema5,ema10) and Strategy.greaterThan(ema10,ema24):
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
        ema54_2 = Strategy.ema_n(rdata,2,54)
        if ema54_2 == 0:
            return False
        ema54_1 = Strategy.ema_pre_n(rdata,ema54_2,1,54)
        ema54_0 = Strategy.ema_pre_n(rdata,ema54_1,0,54)
        if ema54_0>= ema54_1 and ema54_1>=ema54_2:
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

