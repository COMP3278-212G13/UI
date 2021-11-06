import sys
import typing
import mysql.connector

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QCheckBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QSlider, QStackedWidget, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QSize, QTimer, QUrl
from qtwidgets import AnimatedToggle, PasswordEdit

from qt_material import apply_stylesheet

from datetime import datetime


myconn = mysql.connector.connect(host="localhost", user="root", passwd="20010109", database="facerecognition")
cur = myconn.cursor()
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H:%M:%S")


class MainWindow(QMainWindow):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super(MainWindow, self).__init__(parent)
        self.init_UI()

    def init_UI(self):
        self.setWindowIcon(QIcon('logo.png'))
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
        apply_stylesheet(app, theme='light_blue.xml')


class FrontpageWidget(QWidget):
    def __init__(self, parent) -> None:
        super(FrontpageWidget, self).__init__(parent)
        self.init_UI(parent)
        return


    def init_UI(self, parent):
        sp = self.parent()

        # -- Camera video label --
        self.cam_feed = QLabel()
        self.cam_feed.setMinimumSize(640, 480)
        # self.cam_feed.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.cam_feed.setFrameStyle(QFrame.StyledPanel)

        # -- Confidence label --
        self.confi_lbl = QLabel('Confidence: 0')
        self.confi_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.confi_lbl.setContentsMargins(0,8,5,8)

        # -- Confidence slider --
        self.confi_slider = QSlider()
        self.confi_slider.setOrientation(Qt.Orientation.Horizontal)
        self.confi_slider.setTracking(True)

        # -- Customer ID / username label --
        self.uid_lbl = QLabel('User ID')
        self.uid_lbl.setMinimumWidth(70)
        self.uid_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # -- Customer ID / username textbox --
        self.uid_input = QLineEdit()

        # -- Login password label --
        self.pwd_lbl = QLabel('Password')
        self.pwd_lbl.setMinimumWidth(70)
        self.pwd_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # -- login password textbox --
        self.pwd_input = PasswordEdit()

        # -- login / sign up mode select button --
        self.btn_mode = QPushButton("Login / Sign up: Login")
        self.btn_mode.setCheckable(True)
        self.btn_mode.setChecked(False)
        # self.btn_mode_style_0 = 'QPushButton {background-color: #00a86c; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 16px;}'
        # self.btn_mode_style_1 = 'QPushButton {background-color: #ff6464; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 16px;}'
        # self.btn_mode.setStyleSheet(self.btn_mode_style_0)

        
        # -- Face Recognition button --
        self.btn_face = QPushButton('Face Recognition')
        self.btn_face.setCheckable(True)
        self.btn_face.setChecked(False)
        self.btn_face.setIcon(QIcon('facerecognition_logo1.png'))

        # -- Confirm button --
        self.btn_confirm = QPushButton('Confirm')

        # -- Theme label --
        self.theme_lbl = QLabel('Night Mode:')
        self.theme_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # -- Dark theme toggle --
        self.theme_toggle = AnimatedToggle(
            checked_color="#2979ff",
            pulse_checked_color="#442979ff"
        )


        h_box_cam = QHBoxLayout()
        h_box_cam.addWidget(self.cam_feed)

        h_box_confi = QHBoxLayout()
        h_box_confi.addWidget(self.confi_lbl)
        h_box_confi.addWidget(self.confi_slider)

        h_box_uid = QHBoxLayout()
        h_box_uid.addWidget(self.uid_lbl)
        h_box_uid.addWidget(self.uid_input)

        h_box_pwd = QHBoxLayout()
        h_box_pwd.addWidget(self.pwd_lbl)
        h_box_pwd.addWidget(self.pwd_input)

        h_box_btn = QHBoxLayout()
        h_box_btn.addWidget(self.btn_mode)
        h_box_btn.addWidget(self.btn_face)
        h_box_btn.addWidget(self.btn_confirm)

        h_box_theme = QHBoxLayout()
        h_box_theme.setAlignment(Qt.AlignmentFlag.AlignRight)
        h_box_theme.addWidget(self.theme_lbl)
        h_box_theme.addWidget(self.theme_toggle)


        v_box1 = QVBoxLayout()
        v_box1.addLayout(h_box_cam)
        v_box1.addLayout(h_box_confi)
        v_box1.addLayout(h_box_uid)
        v_box1.addLayout(h_box_pwd)
        v_box1.addLayout(h_box_btn)
        v_box1.addLayout(h_box_theme)

        self.setLayout(v_box1)

        # self.btn_confirm.clicked.connect(self.parent().setDarkMode) ###########
        # self.btn_mode.clicked.connect(self.parent().setDarkMode)
        

        self.theme_toggle.stateChanged.connect(lambda: sp.setDarkMode() if self.theme_toggle.isChecked() else sp.setLightMode())
        # self.theme_toggle.

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
    main_window = MainWindow()
    main_window.resize(1280, 720)
    main_window.show()
    sys.exit(app.exec_())