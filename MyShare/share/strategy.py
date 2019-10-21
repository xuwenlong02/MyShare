import pandas as pd
from pandas import DataFrame as df
import datetime

class Strategy(object):
    """description of class"""

    @staticmethod
    def isStrongArranged(rdata):
        """是否均线多头排列"""
        ema5 = Strategy.ema_n(rdata,0,5)
        ema10 = Strategy.ema_n(rdata,0,10)
        ema24 = Strategy.ema_n(rdata,0,24)
        ema54 = Strategy.ema_n(rdata,0,54)
        if ema5 >= ema10 and ema10 > ema24 and ema24 > ema54:
            return True
        return False
    
    @staticmethod
    def isAvlineBone(rdata):
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
        stg = Strategy()
        ma1 = stg.ma_n(rdata,0,n)
        ma2 = stg.ma_n(rdata,1,n)
        try:
            return (ma1-ma2)/rdata.loc[1,'close']
        except:
            print(rdata)
            return -100

