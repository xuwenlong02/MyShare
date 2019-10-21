import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont,QPen,QPaintEvent
from PyQt5.QtCore import Qt,QPoint
from pandas import DataFrame
from share.strategy import Strategy

class TradeTime(QWidget):
    """description of class"""

    def __init__(self):
        super().__init__()
        self.N = 60
        self.top = 1
        self.bodom = -1
        self.pf = None

    def updateData(self,pf):
        self.pf = pf
        if pf is None:
            return
        self.top = pf.ix[0,'high']
        self.bodom = pf.ix[0,'low']
        self.topi = 0
        self.bodomi = 0

        for i in range(1,self.N,1):
            curh =pf.ix[i,'high']
            curl = pf.ix[i,'low']
            if curh > self.top :
                self.top = curh
            if curh < self.bodom :
                self.bodom = curh

            if curl < self.bodom:
                self.bodom = curl
            if curl > self.top:
                self.top = curl
        self.update()

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
        h = event.rect().height()-30
        w = event.rect().width() - 30

        if self.pf is None:
            return

        kw = w/self.N
        kh = h/(self.top-self.bodom)

        #绘制k线

        for i in range(0,self.N,1):
            
            high = self.pf.ix[i,'high']
            low = self.pf.ix[i,'low']
            open = self.pf.ix[i,'open']
            close = self.pf.ix[i,'close']
            pre_close = self.pf.ix[i,'pre_close']
            pct_chg = self.pf.ix[i,'pct_chg']
            #画k线
            if open < close:
                #画K线
                qp.fillRect(15+kw*(self.N-i-1),15+(self.top-close)*kh,kw,(close-open)*kh,QColor(255,0,0))
                #画上下影线
                pen = QPen(QColor(255,0,0),1,Qt.SolidLine)
                qp.setPen(pen)
                qp.drawLine(15+kw*(self.N-i-1)+kw*0.5,15+(self.top-high)*kh,15+kw*(self.N-i-1)+kw*0.5,15+(self.top-low)*kh)
            else:
                #画K线
                if open == close:
                    pen = QPen(QColor(0,0,255),1,Qt.SolidLine)
                    qp.setPen(pen)
                    qp.drawLine(15+kw*(self.N-i-1),15+(self.top-open)*kh,15+kw*(self.N-i-1)+kw,15+(self.top-open)*kh)
                else:
                    qp.fillRect(15+kw*(self.N-i-1),15+(self.top-open)*kh,kw,(open-close)*kh,QColor(0,0,255))
                #画上下影线
                pen = QPen(QColor(0,0,255),1,Qt.SolidLine)
                qp.setPen(pen)
                qp.drawLine(15+kw*(self.N-i-1)+kw*0.5,15+(self.top-high)*kh,15+kw*(self.N-i-1)+kw*0.5,15+(self.top-low)*kh)

        #绘制均线
        #5日
        self.drawMaLine(qp,kw,kh,5,QColor(0,0,0))
        #10日
        self.drawMaLine(qp,kw,kh,10,QColor(255,201,14))
        #24日
        self.drawMaLine(qp,kw,kh,24,QColor(255,0,128))
        #56日
        self.drawMaLine(qp,kw,kh,56,QColor(0,255,64))

    def drawMaLine(self,qp,kw,kh,n,color):
        pen = QPen(color,1,Qt.SolidLine)
        qp.setPen(pen)
        p0 = QPoint(15+kw*(self.N-1)+kw*0.5,15+(self.top-Strategy.ma_n(self.pf,0,n))*kh)
        for i in range(1,self.N,1):
            ma = Strategy.ma_n(self.pf,i,n)
            if ma == 0:
                break
            p1 = QPoint(15+kw*(self.N-i-1)+kw*0.5,15+(self.top-ma)*kh)
            qp.drawLine(p0,p1)
            p0 = p1