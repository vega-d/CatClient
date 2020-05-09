import sys
import threading

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMenu, QAction, qApp, QSystemTrayIcon, QStyle


def server():
    print("Starting up the server")
    try:
        import production_run
    except Exception as e:
        return 'cant find the production release file'
    try:
        production_run.run()
    except Exception as e:
        return 'server crashed. stack:' + str(e)
    print("server shut down")


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.move(180, 100)
        self.setFixedSize(400, 300)
        self.setWindowTitle('control')

        self.server = threading.Thread(target=server)

        self.toclose = False
        self.all_buttons = []

        self.start_button = QPushButton('start/stop', parent=self)
        self.start_button.setGeometry(100, 100, 200, 100)
        self.start_button.action = 'start'
        self.all_buttons.append(self.start_button)

        for i in self.all_buttons:
            i.clicked.connect(self.onClick)

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def onClick(self):
        btn = self.sender().action
        print(btn, 'action released!')
        if btn == 'start':
            if not self.server.is_alive():
                self.server.start()
                self.start_button.setEnabled(0)
                self.start_button.setText('server running')

    def closeEvent(self, evnt):
        if self.toclose:
            super(App, self).closeEvent(evnt)
        else:
            evnt.ignore()
            self.hide()


app = QApplication(sys.argv)
form = App()
form.show()
sys.exit(app.exec())
