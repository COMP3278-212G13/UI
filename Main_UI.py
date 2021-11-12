import sys
import typing

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget

from mysql.connector.connection import MySQLConnection
from qt_material import apply_stylesheet

from FrontpageWidget import FrontpageWidget
from ProfileWidget import ProfileWidget
from Trans import Trans


myconn = MySQLConnection(host="localhost", user="root", passwd="20010109", database="facerecognition", autocommit=True)
cur = myconn.cursor()


userid: str = None
def setUserId(id: str):
    global userid
    userid = id
def getUserId():
    return userid


isDarkTheme: bool = False
def setTheme(isDark: bool):
    global isDarkTheme
    isDarkTheme = isDark
    if isDark:
        apply_stylesheet(app, theme='dark_blue.xml')
    else:
        apply_stylesheet(app, theme='light_blue.xml')


account_id = None
def setAccountId(id: str):
    global account_id
    account_id = id
def getAccountId():
    return account_id


class MainWindow(QMainWindow):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super(MainWindow, self).__init__(parent)
        self.init_UI()

    def init_UI(self):
        self.setWindowIcon(QIcon('assets/logo.png'))
        self.setWindowTitle('Intelligent Know Your Customer')

        self.main_widget = QStackedWidget()
        self.setCentralWidget(self.main_widget)
        frontpage_widget = FrontpageWidget(self, cur, setTheme, setUserId)
        self.main_widget.addWidget(frontpage_widget)

    def setLoggedinWigget(self):
        profile_widget = ProfileWidget(self, cur, getUserId, setAccountId)
        self.main_widget.addWidget(profile_widget)
        self.main_widget.setCurrentWidget(profile_widget)

    def setAccountWidget(self):
        transaction_widget = Trans(self, cur, getAccountId)
        self.main_widget.addWidget(transaction_widget)
        self.main_widget.setCurrentWidget(transaction_widget)

    # logout - return to login page
    def setLoggedout(self):
        self.setWindowTitle('Intelligent Know Your Customer')
        frontpage_widget = FrontpageWidget(self, cur, setTheme, setUserId)
        self.main_widget.addWidget(frontpage_widget)
        self.main_widget.setCurrentWidget(frontpage_widget)
    
    def back(self):
        back = ProfileWidget(self, cur, getUserId, setAccountId)
        self.main_widget.addWidget(back)
        self.main_widget.setCurrentWidget(back)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setTheme(True)
    main_window = MainWindow()
    main_window.resize(1280, 720)
    main_window.show()
    sys.exit(app.exec_())