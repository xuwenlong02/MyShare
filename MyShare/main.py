import sys
from hmi.mainwindow import MainWindow
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())