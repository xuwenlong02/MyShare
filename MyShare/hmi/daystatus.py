import sys
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QListView, QTableView
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QSize
from hmi.tradetime import TradeTime
from hmi.tradevolum import TradeVolum
from hmi.pricelistmodel import PriceListModel
from hmi.tradetitle import TradeTitle
import tushare as ts


class DayStatus(QWidget):
    """description of class"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.titleWidget = TradeTitle()
        self.ttWidget = TradeTime()
        self.tvWidget = TradeVolum()
        # self.tpWidget = QTableView()
        # self.priceModel = PriceListModel()
        # self.tpWidget.setAutoFillBackground(True)
        # self.tpWidget.setGridSize(QSize(15,40))
        # self.tpWidget.setColumnWidth(0,40)
        # self.tpWidget.setColumnWidth(1,80)
        # self.tpWidget.setColumnWidth(2,80)
        # self.tpWidget.setModel(self.priceModel)
        vbox = QVBoxLayout()
        vbox.addWidget(self.titleWidget, 5)
        vbox.addWidget(self.ttWidget, 75)
        vbox.addWidget(self.tvWidget, 20)
        self.setLayout(vbox)

    def activeCode(self, rdata):
        # rdata = ts.get_realtime_quotes('%s'%code)
        self.titleWidget.updateData(rdata)
        self.ttWidget.updateData(rdata)
        self.tvWidget.updateData(rdata)
        # self.priceModel.setData(rdata)
        # self.histData = ts.get_hist_data('%06d'%code,start='2019-09-30',ktype='5')
        # print(self.histData)

