import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp,QWidget, QApplication,QListWidget,QHBoxLayout,QVBoxLayout,QComboBox,QToolBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QModelIndex,Qt, pyqtSignal   
from hmi.timingstatus import TimingStatus

from hmi.sharelistwidget import ShareListWidget
import tushare as ts
import os
import threading
from time import ctime,sleep
import pandas as pd
from pandas import DataFrame as df
from share.avlinebone import AvlineBone
from share.lowsuction import LowSuction
from share.uppershadow import UpperShadow
from share.sharedata import ShareData
import datetime

class MainWindow(QMainWindow):
    """description of class"""

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initData()

    def initUI(self):
        self.statusBar()
        menubar = self.menuBar()
        toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea,toolbar)

        funcMenu = menubar.addMenu('功能')
        upAction = funcMenu.addAction('更新数据')
        upAction.triggered.connect(self.updateData)
        menubar.addMenu(funcMenu)

        self.setGeometry(10,10,800,600)
        self.setWindowIcon(QIcon("image/title.jpg"))
        self.setWindowTitle("行情观察")
        
        self.listWidget = ShareListWidget()
        self.comSelect = QComboBox()
        self.comSelect.addItems(['全部','上影线战法','低吸战法','均线粘合向上'])
        vbox = QVBoxLayout()
        vbox.addWidget(self.comSelect,1)
        vbox.addWidget(self.listWidget,15)
        
        self.tradeWidget = TimingStatus()
        hbox = QHBoxLayout()
        hbox.addLayout(vbox,15)
        hbox.addWidget(self.tradeWidget,85)

        self.comSelect.currentIndexChanged.connect(self.SlotStrategy)
        
        centerWidget = QWidget()
        self.setCentralWidget(centerWidget)
        centerWidget.setLayout(hbox)
        self.listWidget.clicked.connect(self.Slot_ItemClicked)

    def initData(self):
        #print(ts.get_concept_classified())
        #self.stocks = pd.read_csv('./data/stocks.csv',encoding='gbk')
        self.pro = ts.pro_api('604a0f99c257e0a0f3ae4ed6291a99e986f482be8083e561f09622ad')
        self.stocks = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,industry,market')
        self.noticeStocks = self.stocks
        self.listWidget.setData(self.stocks)

    def updateData(self,on:bool):
        sd = ShareData(self.pro,self.stocks)

    def Slot_ItemClicked(self,index):
        code = self.noticeStocks.ix[index.row(),'ts_code']
        types = {'ts_code':object,'trade_date':object,'open':float,
                                                                     'high':float,'low':float,'close':float,'pre_close':float,
                                                         'change':float,'pct_chg':float,'vol':float,'amount':float}
        rdf =  pd.read_csv('./data/%s.csv'%code,encoding='gbk',dtype=types)
        if rdf is None or len(rdf) < 20:
            return
        strtoday = datetime.datetime.now().strftime('%Y%m%d')
        if rdf.loc[0,'trade_date'] != strtoday:
            symbol = self.noticeStocks.ix[index.row(),'symbol']
            tdf = ts.get_realtime_quotes(symbol)
            if tdf is not None:
                strdate = tdf.ix[0,'date']
                if datetime.datetime.strptime(strdate,'%Y-%m-%d') == datetime.datetime.strptime(strtoday,'%Y%m%d'):
                    open = float(tdf.ix[0,'open'])
                    high = float(tdf.ix[0,'high'])
                    low = float(tdf.ix[0,'low'])
                    close = float(tdf.ix[0,'price'])
                    pre_close = float(tdf.ix[0,'pre_close'])
                    vol = float(tdf.ix[0,'volume'])/100
                    amount = float(tdf.ix[0,'amount'])/1000

                    rw = {'ts_code':[code],'trade_date':[datetime.datetime.now().strftime('%Y%m%d')],'open':[open],
                             'high':[high],'low':[low],'close':[close],'pre_close':[pre_close],'change':[0.0],
                             'pct_chg':[(close-pre_close)/pre_close*100],'vol':[vol],'amount':[amount]}
                    df_new = df(data = rw,index=None)
                    # columns = ['ts_code', 'trade_date', 'open', 'high', 'low', 'close',
                    #            'pre_close', 'change', 'pct_chg', 'vol', 'amount']
                    #old = rdf.loc[0:]

                    rdf = df_new.append(rdf,ignore_index=True,sort = True)

        self.tradeWidget.activeCode(rdf)

    def SlotStrategy(self,index):
        if index == 0:
            self.noticeStocks = self.stocks
            self.listWidget.setData(self.stocks)
        elif index == 1:
            #上影线战法
            us = UpperShadow(self.stocks)
            self.noticeStocks = us.resultList()
            self.listWidget.setData(us.resultList())
            
        elif index == 2:
            #低吸战法
            us = LowSuction(self.stocks)
            self.noticeStocks = us.resultList()
            self.listWidget.setData(self.noticeStocks)
        elif index == 3:
            #均线粘合
            us = AvlineBone(self.stocks)
            self.noticeStocks = us.resultList()
            self.listWidget.setData(us.resultList())
