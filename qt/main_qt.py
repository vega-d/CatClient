import sqlite3
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from qt.qt_func import resource_path
import datetime
import sys
from PyQt5.QtCore import Qt


class Main(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.Window)
        if __name__ == '__main__':
            uic.loadUi(resource_path('main_qt.ui'), self)
        else:
            uic.loadUi(resource_path('qt\\main_qt.ui'), self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Admin panel')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main()
    form.show()
    sys.exit(app.exec())
