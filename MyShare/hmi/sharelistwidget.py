import sys
from PyQt5.QtWidgets import QListView,QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QAbstractListModel,QVariant
from hmi.sharelistmodel import ShareListModel


class ShareListWidget(QListView):
    """description of class"""

    def __init__(self):
        super().__init__()
        self.listModel = ShareListModel()
        self.setModel(self.listModel)


    def setData(self,datas):
        self.listModel.setData(datas)
