import sys
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QAbstractListModel,QVariant,QModelIndex,Qt
import numpy as np
from pandas import DataFrame


class ShareListModel(QAbstractListModel):
    """description of class"""

    def __init__(self):
        super().__init__()
        self.listData = DataFrame()
        
    def data(self,index,role):
        if index.isValid() or (0 <= index.row() < len(self.listData)):
            if role != Qt.DisplayRole:
                return QVariant()
            if index.column() == 0:
                return QVariant('%s[%s]'%(self.listData.ix[index.row(),'name'],self.listData.ix[index.row(),'symbol']))
            elif index.column() == 1:
                return QVariant("%s"%self.listData.ix[index.row(),'industry'])
            elif index.column() == 2:
                return QVariant('%0.3f'%self.listData.ix[index.row(),'weight'])
        return QVariant()

    def rowCount(self,parent = QModelIndex()):
        return len(self.listData)

    def columnCount(self,parent = QModelIndex()):
        return 3

    def setData(self,datas):
        if len(self.listData) > 0:
            self.beginRemoveRows(QModelIndex(),0,len(self.listData)-1)
            self.endRemoveRows()
        self.listData = datas
        if len(self.listData) > 0:
            self.beginInsertRows(QModelIndex(),0,len(self.listData)-1)
            self.endInsertRows()