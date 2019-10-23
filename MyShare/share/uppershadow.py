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

        pcg_chg = df.loc[0, 'pct_chg']
        if pcg_chg < -8 and pcg_chg > 8:
            return False

        close = df.loc[0, 'close']
        open = df.loc[0, 'open']
        vol = df.loc[0, 'vol']
        high =df.loc[0,'high']
        low = df.loc[0,'low']
        ul = high-max(open,close)

        emv = Strategy.mv_n(df,1,5)

        if vol >= emv*1.2 and vol < emv*2.5 and ul> 0:
            for i in range(1,10,1):
                if df.loc[i,'high'] > high:
                    return False
            return True
        return False


