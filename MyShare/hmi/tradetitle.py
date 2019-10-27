import sys
from PyQt5.QtWidgets import QWidget, QApplication,QLabel,QGridLayout
from PyQt5.QtGui import QPainter, QColor, QFont,QPen
from PyQt5.QtCore import Qt
from share.strategy import Strategy


class TradeTitle(QWidget):
    """description of class"""

    def __init__(self):
        super().__init__()
        self.labPrice = QLabel("<font color='red' size=40px >6.54</font>")
        self.labPrice.setFont(QFont('微软雅黑',40))
        self.labRate = QLabel("<font color='red'>--%</font>")
        self.labHigh = QLabel("高 <font color='red'>--</font>")
        self.labLow= QLabel("低 <font color='blue'>--</font>")
        self.labOpen = QLabel("开 <font color='blue'>--</font>")
        self.labChange = QLabel("换 <font color='black'>--%</font>")
        self.labVolum = QLabel("量 <font color='black'>--万</font>")
        self.labOver = QLabel("额 <font color='black'>--亿</font>")
        self.labDate = QLabel("")
        self.labWeight = QLabel("权重 <font color='red'>0</font>")
        grid = QGridLayout()
        col = 0
        row = 0
        grid.addWidget(self.labPrice,row,col,3,3)
        grid.addWidget(self.labDate,row+3,col,1,2)
        grid.addWidget(self.labRate,row+3,col+2,1,1)

        col =col+4
        grid.addWidget(self.labHigh,0,col,2,2)
        grid.addWidget(self.labLow,2,col,2,2)
        col = col+2
        grid.addWidget(self.labOpen,0,col,2,2)
        grid.addWidget(self.labWeight,2,col,2,2)
        col = col+2
        grid.addWidget(self.labVolum,0,col,2,2)
        grid.addWidget(self.labOver,2,col,2,2)
        self.setLayout(grid)

    def updateData(self,rdata):
        if rdata is not None:
            self.labDate.setText(rdata.ix[0,'trade_date'])
            price = rdata.ix[0,'close']
            open = rdata.ix[0,'pre_close']
            rate = (price-open)/open;
            if rate > 0:
                self.labPrice.setText("<font color='red'>%0.2f</font>"%rdata.ix[0,'close'])
                self.labRate.setText("<font color='red'>%0.2f%%</font>"%(rdata.ix[0,'pct_chg']))
                self.labHigh.setText("高 <font color='red'>%0.2f</font>"%rdata.ix[0,'high'])
                self.labLow.setText("低 <font color='red'>%0.2f</font>"%rdata.ix[0,'low'])
                self.labOpen.setText("开 <font color='red'>%0.2f</font>"%rdata.ix[0,'open'])
            else:
                self.labPrice.setText("<font color='blue'>%0.2f</font>"%rdata.ix[0,'close'])
                self.labRate.setText("<font color='blue'>%0.2f%%</font>"%(rdata.ix[0,'pct_chg']))
                self.labHigh.setText("高 <font color='blue'>%0.2f</font>"%rdata.ix[0,'high'])
                self.labLow.setText("低 <font color='blue'>%0.2f</font>"%rdata.ix[0,'low'])
                self.labOpen.setText("开 <font color='blue'>%0.2f</font>"%rdata.ix[0,'open'])
                #self.labChange.setText("换 <font color='black'>%s%</font>"%rdata['turnoverratio'])
            volum = rdata.ix[0,'vol']/10000.0
            amount = rdata.ix[0,'amount']/10
            self.labVolum.setText("量 %0.2f万"%volum)
            self.labOver.setText("额 %0.2f万"%amount)
            self.labWeight.setText("权重 <font color='red'>%0.2f</font>"%Strategy.weight(rdata))
        else:
            self.labPrice.setText("--")
            self.labRate.setText("--")
            self.labHigh.setText("高 --")
            self.labLow.setText("低 --")
            self.labOpen.setText("开 --")
            self.labChange.setText("换 --")
            self.labVolum.setText("量 --万")
            self.labOver.setText("额 --万")
        self.labPrice.adjustSize()
        self.labRate.adjustSize()
        self.labHigh.adjustSize()
        self.labLow.adjustSize()
        self.labOpen.adjustSize()
        self.labWeight.adjustSize()
        self.labVolum.adjustSize()
        self.labOver.adjustSize()