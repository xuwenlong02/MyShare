import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp,QWidget, QApplication,QListWidget,QHBoxLayout,QVBoxLayout,QComboBox,QToolBar,QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QModelIndex,Qt, pyqtSignal   
from hmi.timingstatus import TimingStatus
from hmi.daystatus import DayStatus

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
from share.limitforecast import LimitForecast
from share.crossriversea import CrossRiverSea
import datetime
from share.strategy import Strategy


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

        self.setGeometry(10,10,1400,800)
        self.setWindowIcon(QIcon("image/title.jpg"))
        self.setWindowTitle("行情观察")
        
        self.listWidget = ShareListWidget()
        self.comSelect = QComboBox()
        self.comSelect.addItems(['全部','上影线战法','低吸战法','均线粘合向上','涨停式上影线战法','上穿5日线战法'])
        vbox = QVBoxLayout()
        vbox.addWidget(self.comSelect,1)
        vbox.addWidget(self.listWidget,15)

        self.tabWidget = QTabWidget()
        hbox = QHBoxLayout()
        hbox.addLayout(vbox, 14)
        hbox.addWidget(self.tabWidget, 84)
        
        self.timingWidget = TimingStatus()
        self.dayWidget = DayStatus()

        self.tabWidget.addTab(self.timingWidget,u"日")
        self.tabWidget.addTab(self.dayWidget,u"时")
        self.tabWidget.currentChanged.connect(self.SlotTabChanged)


        self.comSelect.currentIndexChanged.connect(self.SlotStrategy)
        
        centerWidget = QWidget()
        self.setCentralWidget(centerWidget)
        centerWidget.setLayout(hbox)
        self.listWidget.clicked.connect(self.Slot_ItemClicked)

    def initData(self):
        self.currentId = -1
        #print(ts.get_concept_classified())
        #self.stocks = pd.read_csv('./data/stocks.csv',encoding='gbk')
        self.pro = ts.pro_api('604a0f99c257e0a0f3ae4ed6291a99e986f482be8083e561f09622ad')
        self.stocks = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,industry,market')
        self.noticeStocks = self.stocks
        self.listWidget.setData(self.stocks)

    def updateData(self,on:bool):
        sd = ShareData(self.pro,self.stocks)

    def SlotTabChanged(self,index):
        if self.currentId == -1:
            return
        code = self.noticeStocks.ix[self.currentId, 'ts_code']
        symbol = self.noticeStocks.ix[self.currentId, 'symbol']
        types = {'ts_code': object, 'trade_date': object, 'open': float,
                 'high': float, 'low': float, 'close': float, 'pre_close': float,
                 'change': float, 'pct_chg': float, 'vol': float, 'amount': float}
        rdf = pd.read_csv('./data/%s.csv' % code, encoding='gbk', dtype=types)
        if rdf is None or len(rdf) < 20:
            return
        rdf = Strategy.nowadayDf(code, symbol, rdf)
        if index == 0:
            self.timingWidget.activeCode(code)
        elif index == 1:
            self.dayWidget.activeCode(rdf)

    def Slot_ItemClicked(self,index):
        self.currentId = index.row()
        self.SlotTabChanged(self.tabWidget.currentIndex())

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
        elif index == 4:
            #均线粘合
            us = LimitForecast(self.stocks)
            self.noticeStocks = us.resultList()
            self.listWidget.setData(us.resultList())
        elif index == 5:
            us = CrossRiverSea(self.stocks)
            self.noticeStocks = us.resultList()
            self.listWidget.setData(us.resultList())
