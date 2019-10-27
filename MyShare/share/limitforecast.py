import pandas as pd
from pandas import DataFrame
from share.strategy import Strategy
import datetime
import os
import threading
from time import ctime,sleep

class LimitForecast(Strategy):
    """description of class"""

    def IsCorporate(self,df):
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
            if self.is_highest(0,df):
                return self.is_limit(df)
        return False


        
   
    def is_limit(self,df):
        ema5 = Strategy.ma_n(df,0,5)
        ema13 = Strategy.ma_n(df,0,13)
        ema24 = Strategy.ma_n(df,0,24)
        ema54 = Strategy.ma_n(df,0,54)

        if ema5 == 0 or ema13 == 0 or ema24 == 0 or ema54 == 0:
            return False
        if ema5>ema13>ema24>ema54:
            return False
        limit = df.loc[0,'close']*(1.1)

        ema5 = (Strategy.ma_n(df,0,4)*4+limit)/5
        ema13 = (Strategy.ma_n(df,0,12)*12+limit)/13
        ema24 = (Strategy.ma_n(df,0,23)*23+limit)/24
        ema54 = (Strategy.ma_n(df,0,53)*53+limit)/54

        if ema5>=ema13>=ema24>=ema54:
            return True
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