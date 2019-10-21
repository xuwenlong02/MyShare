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
        return False

