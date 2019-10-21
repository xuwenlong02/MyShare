import sys
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QAbstractTableModel,QVariant,QModelIndex,Qt,QSize
import numpy as np
from pandas import DataFrame


class PriceListModel(QAbstractTableModel):
    """description of class"""

    def __init__(self):
        super().__init__()
        self.listPrice = []
        self.listVolumn = []
        self.listName = ['卖5','卖4','卖3','卖2','卖1','买1','买2','买3','买4','买5']

    def isNumber(data):
        try:
            float(data)
        except TypeError:
            return False
        except ValueError:
            return False
        except Exception as e:
            return False
        else:
            return True
        
    def data(self,index,role):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return QVariant(self.listName[index.row()])
            elif index.column() == 1:
                if (0 <= index.row() < len(self.listPrice)):
                    if isNumber(self.listPrice[index.row()]):
                        price = float(self.listPrice[index.row()])
                        return QVariant(price)
                return QVariant('--')
            elif index.column() == 2:
                if (0 <= index.row() < len(self.listVolumn)):
                    if isNumber(self.listVolumn[index.row()]):
                        volum = float(self.listVolumn[index.row()])
                return QVariant('--')
        return QVariant()

    def rowCount(self,parent = QModelIndex()):
        return 10

    def columnCount(self,parent = QModelIndex()):
        return 3

    def setData(self,rdata):
        if len(self.listPrice) > 0:
            self.beginRemoveRows(QModelIndex(),0,10-1)
            self.endRemoveRows()
        if rdata is None:
            return
        self.listPrice.clear()
        self.listVolumn.clear()
        if rdata.ix[0,'a5_p'] is not None:
            self.listPrice.append(rdata.ix[0,'a5_p'])
            self.listVolumn.append(rdata.ix[0,'a5_v'])
        else:
            self.listPrice.append('-')
            self.listVolumn.append('-')
        if rdata.ix[0,'a4_p'] is not None:
            self.listPrice.append(rdata.ix[0,'a4_p'])
            self.listVolumn.append(rdata.ix[0,'a4_v'])
        else:
            self.listPrice.append('-')
            self.listVolumn.append('-')
        if rdata.ix[0,'a3_p'] is not None:
            self.listPrice.append(rdata.ix[0,'a3_p'])
            self.listVolumn.append(rdata.ix[0,'a3_v'])
        else:
            self.listPrice.append('-')
            self.listVolumn.append('-')
        if rdata.ix[0,'a2_p'] is not None:
            self.listPrice.append(rdata.ix[0,'a2_p'])
            self.listVolumn.append(rdata.ix[0,'a2_v'])
        else:
            self.listPrice.append('-')
            self.listVolumn.append('-')
        if rdata.ix[0,'a1_p'] is not None:
            self.listPrice.append(rdata.ix[0,'a1_p'])
            self.listVolumn.append(rdata.ix[0,'a1_v'])
        else:
            self.listPrice.append('-')
            self.listVolumn.append('-')
        if rdata.ix[0,'b1_p'] is not None:
            self.listPrice.append(rdata.ix[0,'b1_p'])
            self.listVolumn.append(rdata.ix[0,'b1_v'])
        else:
            self.listPrice.append('-')
            self.listVolumn.append('-')
        if rdata.ix[0,'b2_p'] is not None:
            self.listPrice.append(rdata.ix[0,'b2_p'])
            self.listVolumn.append(rdata.ix[0,'b2_v'])
        else:
            self.listPrice.append('-')
            self.listVolumn.append('-')
        if rdata.ix[0,'b3_p'] is not None:
            self.listPrice.append(rdata.ix[0,'b3_p'])
            self.listVolumn.append(rdata.ix[0,'b3_v'])
        else:
            self.listPrice.append('-')
            self.listVolumn.append('-')
        if rdata.ix[0,'b4_p'] is not None:
            self.listPrice.append(rdata.ix[0,'b4_p'])
            self.listVolumn.append(rdata.ix[0,'b4_v'])
        else:
            self.listPrice.append('-')
            self.listVolumn.append('-')
        if rdata.ix[0,'b5_p'] is not None:
            self.listPrice.append(rdata.ix[0,'b5_p'])
            self.listVolumn.append(rdata.ix[0,'b5_v'])
        else:
            self.listPrice.append('-')
            self.listVolumn.append('-')
        if len(self.listPrice) > 0:
            self.beginInsertRows(QModelIndex(),0,10-1)
            self.endInsertRows()