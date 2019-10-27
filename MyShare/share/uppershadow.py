import pandas as pd
from pandas import DataFrame
from share.strategy import Strategy
import datetime
import os
import threading
from time import ctime,sleep

class UpperShadow(Strategy):
    """description of class"""
    
    def IsCorporate(self,df):
        """1、今日放量，至少比前几日高，且有上影线 2、
         n日内横盘 3、n+1日之前两天涨幅出现过大于6%以上 4、多头排列就算了"""
        #if not Strategy.isStrongArranged(df):
        #    return False
        pcg_chg = df.loc[0, 'pct_chg']
        if pcg_chg < -8 and pcg_chg > 8:
            return False
        pre_close = df.loc[0, 'pre_close']
        close = df.loc[0,'close']
        open = df.loc[0, 'open']
        vol = df.loc[0, 'vol']
        #low = df.loc[0,'low']
        ul = df.loc[0,'high']-max(open,close)

        
        #emv = df.loc[1,'vol']
        if close > pre_close:
            return self.is_highest(0,df)
        else:
            emv = Strategy.mv_n(df,0,5)
            if ul > 0 and vol < emv:
                for i in range(1,4,1):
                    if self.is_highest(i,df):
                        return True
                return False
        return False

    def is_highest(self,k,df):
        pre_close = df.loc[k, 'pre_close']
        vol = df.loc[k, 'vol']
        high =df.loc[k,'high']+pre_close*0.01
        close = df.loc[k,'close']
        open = df.loc[k, 'open']
        ul = df.loc[k,'high']-max(open,close)
        emv = Strategy.mv_n(df,k,5)

        if ul > 0 and vol >=1.8*emv and vol <= 4*emv:
            for i in range(k+1,20+k,1):
                if df.loc[i,'high'] > high or df.loc[i,'vol'] > vol*(1.01):
                    return False
            return True
        return False
