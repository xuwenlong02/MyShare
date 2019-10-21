import sys
from PyQt5.QtWidgets import QWidget, QApplication,QHBoxLayout,QVBoxLayout,QListView,QTableView
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt,QSize
from hmi.tradetime import TradeTime
from hmi.tradevolum import TradeVolum
from hmi.pricelistmodel import PriceListModel
from hmi.tradetitle import TradeTitle
import tushare as ts

class dayk(QWidget):
    """description of class"""

    def __init__(self):
        super().__init__()
        self.top = 1
        self.bodom = -1
        self.zero = 0
        self.cdata = DataFrame()

    def updateData(self,top,bodom,zero,cdata):
        self.top = top
        self.bodom = bodom
        self.zero = zero
        self.cdata = cdata

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        
        self.drawBackground(qp,event)
        self.drawCurve(qp,event)
        qp.end()

    def drawBackground(self,qp:QPainter,event:QPaintEvent):
        qp.fillRect(event.rect(),QColor(255,255,255))
        pen = QPen(QColor(223,223,223),1,Qt.SolidLine)
        qp.setPen(pen)
        x1 = 15
        y1= 15
        x2 = event.rect().width()-30
        y2 = event.rect().height()-30
        qp.drawLine(x1,y1,x2,y1)
        qp.drawLine(x2,y1,x2,y2)
        qp.drawLine(x1,y1,x1,y2)
        qp.drawLine(x1,y2,x2,y2)

        pen = QPen(QColor(223,223,223),1,Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(x1,(y1+y2)/4,x2,(y1+y2)/4)
        qp.drawLine(x1,(y1+y2)*3/4,x2,(y1+y2)*3/4)
        qp.drawLine((x1+x2)/4,y1,(x1+x2)/4,y2)
        qp.drawLine((x1+x2)/2,y1,(x1+x2)/2,y2)
        qp.drawLine((x1+x2)*3/4,y1,(x1+x2)*3/4,y2)
        pen = QPen(QColor(0,0,0),1,Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(x1,(y1+y2)/2,x2,(y1+y2)/2)
    
    def drawCurve(self,qp:QPainter,event:QPaintEvent):
        pass


