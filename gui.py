import os
import sys
import typing

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QWidget

from qt_material import apply_stylesheet


class MainWindow(QMainWindow):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super(MainWindow, self).__init__(parent)
        self.init_UI()

    def init_UI(self):
        # self.setStyleSheet('QWidget {background-color: #ffffff;}')
        self.setWindowIcon(QtGui.QIcon('logo.jpg'))
        self.setWindowTitle('Intelligent Know Your Customer')

        self.main_widget = QStackedWidget() ###########
        self.setCentralWidget(self.main_widget) ###########
        frontpage_widget = FrontpageWidget(self)
        # frontpage_widget.button.clicked.connect(self.login)
        self.main_widget.addWidget(frontpage_widget)

    def login(self):
        accounts_widget = AccountsWidget(self) ###########
        self.main_widget.addWidget(accounts_widget) ###########
        self.main_widget.setCurrentWidget(accounts_widget) ###########

    def setDarkMode(self):
        apply_stylesheet(app, theme='dark_blue.xml')

    def setLightMode(self):
        apply_stylesheet(app, theme='dark_blue.xml')



class FrontpageWidget(QWidget):
    def __init__(self, parent) -> None:
        super(FrontpageWidget, self).__init__(parent)
        self.init_UI(parent)
        return


    def init_UI(self, parent):
        self.btn_mode = QPushButton("dark mode")
        self.btn_mode.setMinimumHeight(40)
        self.btn_mode.setCheckable(True)
        self.btn_mode.setChecked(True)
        # self.btn_mode_style_0 = 'QPushButton {background-color: #00a86c; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 16px;}'
        # self.btn_mode_style_1 = 'QPushButton {background-color: #ff6464; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 16px;}'
        # self.btn_mode.setStyleSheet(self.btn_mode_style_0)

        self.btn_login = QPushButton('Login')
        self.btn_login.setMinimumHeight(40)

        h_box_conn = QHBoxLayout()
        h_box_conn.addWidget(self.btn_mode)
        h_box_conn.addWidget(self.btn_login)


        v_box1 = QVBoxLayout()
        v_box1.addLayout(h_box_conn)

        self.setLayout(v_box1)

        self.btn_login.clicked.connect(self.parent().login) ###########
        self.btn_mode.clicked.connect(self.parent().setDarkMode)

        return

class AccountsWidget(QWidget):
    def __init__(self, parent) -> None:
        super(AccountsWidget, self).__init__(parent)
        self.init_UI()
        return


    def init_UI(self):
        self.logged = QPushButton('Logged in!!!')
        self.logged.setMinimumHeight(40)

        h_box_conn = QHBoxLayout()
        h_box_conn.addWidget(self.logged)

        v_box1 = QVBoxLayout()
        v_box1.addLayout(h_box_conn)

        self.setLayout(v_box1)

        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')
    # app.setStyle('Fusion')
    main_window = MainWindow()
    main_window.setMinimumSize(1280, 720)
    main_window.show()
    sys.exit(app.exec_())
    # gui.setFixedSize(1600, 1000)