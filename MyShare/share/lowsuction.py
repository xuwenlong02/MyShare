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
        if not Strategy.isStrongArranged(df):
           return False
        pcg_chg = df.loc[0,'pct_chg']
        if pcg_chg < -7 and pcg_chg > 7:
            return False
        close = df.loc[0,'close']
        open = df.loc[0,'open']
        vol = df.loc[0,'vol']
        high = max(close,open)
        low = min(close,open)

        #需要有下影线
        if df.loc[0,'low'] < low:
            for i in range(1,7,1):
                if (df.loc[i,'close'] > close and df.loc[i,'vol']>vol) or (df.loc[i,'close'] <= close and df.loc[i,'vol']<=vol) :
                    close = df.loc[i,'close']
                    open = df.loc[i,'open']
                    vol = df.loc[i,'vol']
                    pre_close = df.loc[i,'pre_close']
                    pcg_chg = df.loc[i,'pct_chg']

                    if pcg_chg > 5 and pre_close <= low and close >= high:
                        return True
                    high = max(close,open,high)
                    low = min(close,open,low)
                else:
                    return False
            return False
        else:
            return False