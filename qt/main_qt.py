import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication

from qt.qt_func import resource_path
from data import db_session
from data.users import User


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
        # ----------------- List_user -----------------

        session = db_session.create_session()
        users = session.query(User).all()
        del users[0]
        self.list_user.addItems(users)
        self.bselect_user.clicked.connect(self.select_user)
        # ----------------- List_dirs -----------------
        self.bselect_dir.clicked.connect(self.select_dir)

    def select_user(self):
        user = self.list_user.currentText()
        session = db_session.create_session()
        users = session.query(User).filter(User.name == user).first()
        if users:
            dirs = users.dirs.split(',')
            self.list_dirs.addItems(dirs)

    def select_dir(self):
        None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main()
    form.show()
    sys.exit(app.exec())
