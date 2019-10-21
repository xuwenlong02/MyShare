import pandas as pd
from pandas import DataFrame
from share.avlinebone import AvlineBone
from share.uppershadow import UpperShadow
from share.strategy import Strategy
import datetime
import os
import threading
from time import ctime, sleep


def threadUpdateData(ls, row):
    ls.UpdateData(row)


class ShareData(object):
    """description of class"""

    def __init__(self, pro, rdata):
        self.pro = pro
        self.rdata = rdata
        self.liData = DataFrame()
        liThs = []
        length = len(rdata)
        for i in range(0, length, 200):
            # 测试
            if i + 50 <= length:
                th = threading.Thread(name='%d' % i, target=threadUpdateData, args=(self, self.rdata[i:i + 200]))
            else:
                th = threading.Thread(name='%d' % i, target=threadUpdateData, args=(self, self.rdata[i:-1]))

            liThs.append(th)
            th.start()
            sleep(65)

        for th in liThs:
            th.join(30)
        print('更新完成!')

    def UpdateData(self, piece):
        """特点：均线多头，近7天内涨幅出现过大于7%，
        之后一直调整且缩量，且没有突破5日均线,
        最好有长上影线和长下影线
        """
        for index, row in piece.iterrows():
            code = row['ts_code']
            df = self.pro.daily(ts_code=code, start_date='20190101',
                                end_date=datetime.datetime.now().strftime('%Y%m%d'))
            if df is None or len(df) == 0:
                continue
            df.to_csv("./data/%s.csv"%code,encoding='gbk')