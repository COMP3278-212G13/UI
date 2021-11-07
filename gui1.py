import sys
import typing

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QSlider, QStackedWidget, QVBoxLayout, QWidget, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from mysql.connector.connection import MySQLConnection
from qtwidgets import AnimatedToggle, PasswordEdit
from qt_material import apply_stylesheet
from datetime import datetime, timedelta, timezone


myconn = MySQLConnection(host="localhost", user="root", passwd="chenjiakai2001", database="facerecognition", autocommit=True)
cur = myconn.cursor()

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
        profile_widget = ProfileWidget(self) ###########
        self.main_widget.addWidget(profile_widget) ###########
        self.main_widget.setCurrentWidget(profile_widget) ###########


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
            cur.execute(f"""Select login_date, login_time, name From Customer WHERE customer_id = "{uid}" AND password = "{self.pwd_input.text()}" """)
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

class ProfileWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.init_window(parent)
        self.show()
    
    def init_window(self, parent):
        sql = "SELECT name, login_date, login_time FROM customer WHERE customer_id = " + userid
        cur.execute(sql)
        row = cur.fetchone()
        cname = row[0]
        last_date = str(row[1])
        last_time = str(row[2])
        
        # window title
        self.setWindowTitle("Profile Overview--" + cname)
        self.resize(600, 400)
        self.move(0, 0)
        
        # welcome msg
        welcome_label = QLabel(self)
        welcome_label.setText("Welcome, dear " + cname + "!")
        #welcome_label.setFont(QFont("Calibri", 20, QFont.Bold))
        welcome_label.move(0, 0)
        
        # display username
        name_label = QLabel(self)
        name_label.setText("Username: " + cname)
        name_label.move(0, 50)

        # display last login time
        login_label = QLabel(self)
        login_label.setText("Last login: " + last_date + " " + last_time)
        login_label.move(200, 50)

        # accounts title
        acct_label = QLabel(self)
        acct_label.setText("Your Accounts:    Double click to check account details")
        acct_label.move(0, 80)

        # table of accounts
        sql = '''
            SELECT *
            FROM (
            SELECT A.account_id AS account_id, A.type AS type, A.currency AS currency, CR.bill AS balance_or_bill
		    FROM account A, credit CR
		    WHERE (
	            A.customer_id = %s
				AND A.account_id = CR.account_id
		    )
		    ) AS temp1 UNION (
		    SELECT A.account_id AS account_id, A.type AS type, A.currency AS currency, CU.balance AS balance_or_bill
		    FROM account A, current CU
		    WHERE (
	            A.customer_id = %s
				AND A.account_id = CU.account_id
		    )
		    )  UNION (
		    SELECT A.account_id AS account_id, A.type AS type, A.currency AS currency, S.balance AS balance_or_bill
		    FROM account A, saving S
		    WHERE (
	            A.customer_id = %s
				AND A.account_id = S.account_id
	        )
		    ) ORDER BY account_id'''
        input = (userid, userid, userid)
        cur.execute(sql, input)
        data = ()
        data = cur.fetchall()
        if data:
            table = QTableWidget(self)
            table.setColumnCount(4)
            table.setRowCount(len(data))
            table.setHorizontalHeaderLabels(["Account ID", "Account Type", "Currency", "Balance/Bill"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            #table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.setSelectionBehavior(QAbstractItemView.SelectRows)
            for i in range(len(data)):
                for j in range(4):
                    item = QTableWidgetItem()
                    item.setText(str(data[i][j]))
                    table.setItem(i, j, item)
            table.move(0, 100)
            table.resize(1000, 1000)
            table.verticalHeader().setVisible(False)
        else:
            nf_label = QLabel(self)
            nf_label.setText("Sorry! You have no account!")
            nf_label.move(0, 100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')
    main_window = MainWindow()
    main_window.resize(1280, 720)
    main_window.show()
    sys.exit(app.exec_())