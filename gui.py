import sys
import typing
import cv2

from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox, QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QSlider, QStackedWidget, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt

from mysql.connector.connection import MySQLConnection
from qtwidgets import AnimatedToggle, PasswordEdit
from qt_material import apply_stylesheet
from datetime import datetime, timedelta, timezone


myconn = MySQLConnection(host="localhost", user="root", passwd="20010109", database="facerecognition", autocommit=True)
cur = myconn.cursor()

faceCascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

userid: str = None


class MainWindow(QMainWindow):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super(MainWindow, self).__init__(parent)
        self.init_UI()

    def init_UI(self):
        self.setWindowIcon(QIcon('assets/logo.png'))
        self.setWindowTitle('Intelligent Know Your Customer')

        self.main_widget = QStackedWidget() ###########
        self.setCentralWidget(self.main_widget) ###########
        frontpage_widget = FrontpageWidget(self)
        self.main_widget.addWidget(frontpage_widget)

    def setLoggedinWigget(self):
        accounts_widget = AccountsWidget(self) ###########
        self.main_widget.addWidget(accounts_widget) ###########
        self.main_widget.setCurrentWidget(accounts_widget) ###########


class FrontpageWidget(QWidget):
    def __init__(self, parent) -> None:
        super(FrontpageWidget, self).__init__(parent)
        self.init_UI(parent)
        return


    def init_UI(self, parent):
        sp = self.parent()
        self.device = None

        # -- Camera video label --
        self.cam_feed = QLabel()
        self.cam_feed.setMinimumSize(640, 480)
        self.cam_feed.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # -- Confidence label --
        self.confi_lbl = QLabel('Confidence: 60')
        self.confi_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.confi_lbl.setMinimumWidth(110)
        self.confi_lbl.setContentsMargins(0,8,0,8)

        # -- Confidence slider --
        self.confi_slider = QSlider(Qt.Orientation.Horizontal)
        self.confi_slider.setRange(0, 100)
        self.confi_slider.setSingleStep(1)
        self.confi_slider.setValue(60)
        self.confi_slider.setTracking(True)

        # -- Customer ID / username label --
        self.uid_lbl = QLabel('User ID')
        self.uid_lbl.setMinimumWidth(75)
        self.uid_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # -- Customer ID / username textbox --
        self.uid_input = QLineEdit()

        # -- Login password label --
        self.pwd_lbl = QLabel('Password')
        self.pwd_lbl.setMinimumWidth(75)
        self.pwd_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # -- login password textbox --
        self.pwd_input = PasswordEdit()

        # -- login / sign up mode select button --
        self.btn_mode = QPushButton("Login / Sign up: Log in  ")
        self.btn_mode.setCheckable(True)
        self.btn_mode.setChecked(False)
        
        # -- Face Recognition button --
        self.btn_face = QPushButton('Face Login')
        self.btn_face.setCheckable(True)
        self.btn_face.setChecked(False)
        self.btn_face.setIcon(QIcon('assets/facerecognition_logo1.png'))

        # -- Confirm button --
        self.btn_confirm = QPushButton('Log in!')

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
        
        self.theme_toggle.stateChanged.connect(lambda: apply_stylesheet(app, theme='dark_blue.xml') if self.theme_toggle.isChecked() else apply_stylesheet(app, theme='light_blue.xml'))
        self.confi_slider.valueChanged.connect(self.sliderChange)
        self.btn_mode.released.connect(self.modeChange)
        self.btn_confirm.clicked.connect(lambda: self.signup() if self.btn_mode.isChecked() else self.login(sp))
        self.btn_face.clicked.connect(self.face)

        return
    

    def sliderChange(self):
        self.confi_lbl.setText(f'Confidence: {self.confi_slider.value()}')


    def modeChange(self):
        if self.btn_mode.isChecked():
            self.btn_mode.setText("Login / Sign up: Sign up")
            self.uid_lbl.setText('Username')
            self.btn_face.setText("Face Register")
            self.btn_confirm.setText("Sign up!")
        else:
            self.btn_mode.setText("Login / Sign up: Log in  ")
            self.uid_lbl.setText('User ID')
            self.btn_face.setText("Face Login")
            self.btn_confirm.setText("Log in!")


    def signup(self):
        username = self.uid_input.text()
        pwd = self.pwd_input.text()
        if username == '':
            QMessageBox.warning(self, "Sign up", "<font size = 5>Sign up failed!<p><font size = 3>Please input username", QMessageBox.Close)
        elif pwd == '':
            QMessageBox.warning(self, "Sign up", "<font size = 5>Sign up failed!<p><font size = 3>Please input password", QMessageBox.Close)
        elif len(username) > 50:
            QMessageBox.warning(self, "Sign up", "<font size = 5>Sign up failed!<p><font size = 3>Username length exceed limit 50", QMessageBox.Close)
        elif len(pwd) > 70:
            QMessageBox.warning(self, "Sign up", "<font size = 5>Sign up failed!<p><font size = 3>Password length exceed limit 70", QMessageBox.Close)
        else:
            gmt8dt = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
            cur.execute("INSERT INTO Customer VALUES(null, %s, SHA2(%s, 224), %s, %s)", (username, pwd, gmt8dt.strftime("%Y-%m-%d"), gmt8dt.strftime("%H:%M:%S")))
            cur.execute("SELECT last_insert_id()")
            uid = cur.fetchone()[0]
            QMessageBox.about(self, "Sign up", f"<font size = 5>Sign up successfully!<p><font size = 3>Hello {username}~ Welcome to iKYC<p><font size = 3>Your user ID is: {uid}<p><font size = 4>Please use your user ID to log in")
            self.btn_mode.setChecked(False)
            self.modeChange()
            self.uid_input.setText(str(uid))

    
    def login(self, parent):
        uid = self.uid_input.text()
        if uid.isnumeric():
            cur.execute(f"""Select login_date, login_time, name From Customer WHERE customer_id = "{uid}" AND password = SHA2("{self.pwd_input.text()}", 224)""")
            result = cur.fetchall()
            if result:
                self.loginSucc(uid, result[0], parent)
            else:
                QMessageBox.warning(self, "Warning", "<font size = 5>Login failed!<p><font size = 3>User ID or password incorrect<p><font size = 3>Please check your input", QMessageBox.Close)
        else:
            QMessageBox.warning(self, "Warning", "<font size = 5>Login failed!<p><font size = 3>User ID should be a number<p><font size = 3>Please check your input", QMessageBox.Close)


    def loginSucc(self, uid, result, parent):
        global userid
        userid = uid
        gmt8dt = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
        current_date = gmt8dt.strftime("%Y-%m-%d")
        current_time = gmt8dt.strftime("%#H:%M:%S")
        cur.execute("UPDATE Customer SET login_date = %s, login_time = %s WHERE customer_id = %s", (current_date, current_time, uid))
        (last_date, last_time, name) = (result[0], result[1], result[2])
        QMessageBox.about(self, "Log in", f"<font size = 5>Welcome {name}!<p><font size = 3>Login time: {current_date} {current_time}<p><font size = 3>Last login: {last_date} {last_time}")
        parent.setLoggedinWigget()

    
    def face(self):
        if self.btn_face.isChecked():
            self.conn_cam()
            self.timer = QTimer()
            self.timer.timeout.connect(self.update)
            self.timer.start(50)
            if self.btn_mode.isChecked():  # signup
                1
            else:  # login
                2
        else:
            self.disconn_cam()
            if self.btn_mode.isChecked():  # signup
                3
            else:  # login
                4

    def conn_cam(self):
        self.device = cv2.VideoCapture(0)

    def disconn_cam(self):
        2

    def update(self):
        Qframe = cv2.cvtColor(self.device.read()[1], cv2.COLOR_BGR2RGB)
        self.cam_feed.setPixmap(QPixmap.fromImage(QImage(Qframe, Qframe.shape[1], Qframe.shape[0], Qframe.strides[0], QImage.Format_RGB888)))
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