import pandas as pd
from pandas import DataFrame
from share.strategy import Strategy
import datetime
import os
import threading
from time import ctime,sleep

class CrossRiverSea(Strategy):
    """description of class"""

    def IsCorporate(self,df):
        if not self.isStrongArranged(df):
            return False
        pre_close = df.loc[0, 'pre_close']
        close = df.loc[0, 'close']
        open = df.loc[0, 'open']
        vol = df.loc[0, 'vol']
        low = df.loc[0,'low']
        ul = df.loc[0, 'high'] - max(open, close)

        am5 = self.ma_n(df,0,5)
        am13 = self.ma_n(df,0,13)

        if am5 >= am13 and am5<close and open < am5 and ul > 0:
            return True
        return False