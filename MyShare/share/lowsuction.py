import pandas as pd
from pandas import DataFrame
from share.strategy import Strategy
import datetime
import os
import threading
from time import ctime,sleep


class LowSuction(Strategy):
    """description of class"""

    def IsCorporate(self,df):
        """特点：均线多头，近7天内涨幅出现过大于7%，
        之后一直调整且缩量，且没有突破5日均线,
        最好有长上影线和长下影线
        """
        if not self.isStrongArranged(df):
            return False
        pcg_chg = df.loc[0,'pct_chg']
        if pcg_chg < -7 and pcg_chg > 7:
            return False
        close = df.loc[0,'close']
        open = df.loc[0,'open']
        high = max(close,open)
        low = min(close,open)
        
        for i in range(1,7,1):
            close = df.loc[i,'close']
            open = df.loc[i,'open']
            pre_close = df.loc[i,'pre_close']
            pcg_chg = df.loc[i,'pct_chg']
            if pcg_chg > 5 and pre_close <= low and close >= high:
                return True
            high = max(close,open,high)
            low = min(close,open,low)
        return False