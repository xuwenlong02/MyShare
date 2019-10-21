import pandas as pd
from pandas import DataFrame
from share.avlinebone import AvlineBone
from share.uppershadow import UpperShadow
from share.strategy import Strategy
import datetime
import os
import threading
from time import ctime,sleep

def runStrategy(ls,row):
    ls.ExecuteStategy(row)

class LowSuction(object):
    """description of class"""

    def __init__(self,pro,rdata):
        self.pro = pro
        self.rdata = rdata
        self.liData = DataFrame()
        liThs = []
        length = len(rdata)
        for i in range(0,length,50):
            #测试
            if i+50 <= length:
                th = threading.Thread(name='%d'%i,target = runStrategy,args=(self,self.rdata[i:i+50]))
            else:
                th = threading.Thread(name='%d'%i,target = runStrategy,args=(self,self.rdata[i:-1]))

            liThs.append(th)
            th.start()  
            

        for th in liThs:
            th.join(30)

    def resultList(self):
        return self.liData

    def ExecuteStategy(self,piece):
        """特点：均线多头，近7天内涨幅出现过大于7%，
        之后一直调整且缩量，且没有突破5日均线,
        最好有长上影线和长下影线
        """
        stg = Strategy()
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
            if stg.isStrongArranged(df):
                for i in range(1,7,1):
                    close = df.loc[i,'close']
                    pre_close = df.loc[i,'pre_close']
                    inc = (close-pre_close)/pre_close
                    if

                self.liData = self.liData.append(row, ignore_index=True)

        