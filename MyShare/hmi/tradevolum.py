import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont,QPen,QPaintEvent
from PyQt5.QtCore import Qt,QPoint
from share.strategy import Strategy

class TradeVolum(QWidget):
    """description of class"""

    def __init__(self):
        super().__init__()
        self.pf = None
        self.max = 1
        self.min = 0
        self.N = 60

    def updateData(self,rdata):
        self.pf = rdata
        if rdata is None:
            return
        self.max = 0
        self.min = 0
        for i in range(0,self.N,1):
            if rdata.ix[i,'vol'] > self.max:
                self.max = rdata.ix[i,'vol']
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
        pen.setStyle(Qt.DotLine)

        qp.drawLine((x1+x2)/4,y1,(x1+x2)/4,y2)
        qp.drawLine((x1+x2)/2,y1,(x1+x2)/2,y2)
        qp.drawLine((x1+x2)*3/4,y1,(x1+x2)*3/4,y2)
        pen = QPen(QColor(0,0,255),1,Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(x1,(y1+y2)/2,x2,(y1+y2)/2)

    def drawCurve(self,qp:QPainter,event:QPaintEvent):
        h = event.rect().height()-30
        w = event.rect().width() - 30

        if self.pf is None:
            return

        kw = w/self.N
        kh = h/(self.max-self.min)

        #绘制量能线
        for i in range(0,self.N,1):
            volum = self.pf.ix[i,'vol']
            pct_chg = self.pf.ix[i,'pct_chg']
            if pct_chg >= 0:
                qp.fillRect(15+kw*(self.N-i-1),15+(self.max-volum)*kh,kw,(volum)*kh,QColor(255,0,0))
            else:
                qp.fillRect(15+kw*(self.N-i-1),15+(self.max-volum)*kh,kw,(volum)*kh,QColor(0,0,255))

        #绘制均线
        self.drawMaLine(qp,kw,kh,5,QColor(0,0,0))
        self.drawMaLine(qp,kw,kh,10,QColor(255,0,128))

    def drawMaLine(self,qp,kw,kh,n,color):
        pen = QPen(color,1,Qt.SolidLine)
        qp.setPen(pen)
        p0 = QPoint(15+kw*(self.N-1)+kw*0.5,15+(self.max-Strategy.mv_n(self.pf,0,n))*kh)
        for i in range(1,self.N,1):
            ma = Strategy.mv_n(self.pf,i,n)
            if ma == 0:
                break
            p1 = QPoint(15+kw*(self.N-i-1)+kw*0.5,15+(self.max-ma)*kh)
            qp.drawLine(p0,p1)
            p0 = p1
