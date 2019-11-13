import pandas as pd
from pandas import DataFrame
from share.strategy import Strategy
import datetime
import os
import threading
from time import ctime,sleep

class AvlineBone(Strategy):
    """description of class"""

    def IsCorporate(self,df):
       if Strategy.weight(df) > 0:
           return True
       return False
