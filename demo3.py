# -*- coding: utf-8 -*-

import os
import sys
import cv2
import mysql.connector
from datetime import datetime

# 1 Create database connection
myconn = mysql.connector.connect(host="localhost", user="root", passwd="111111", database="facerecognition")
cur = myconn.cursor()
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H:%M:%S")

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, QTimer, QUrl
from PyQt5.QtGui import QIcon, QImage, QMovie, QPixmap, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QWidget
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QDialog, QDialogButtonBox, QFormLayout


class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);
        
        layout = QFormLayout(self)
        layout.addRow("Username", self.first)
        layout.addRow("Password", self.second)
        layout.addWidget(buttonBox)
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
    
    def getInputs(self):
        return (self.first.text(), self.second.text())


# MainGUI class
class MainGUI(QWidget):

    # ~~~~~~~~ constructor ~~~~~~~~
    def __init__(self):
        super().__init__()
        self.init_UI()
        
        return

    # ~~~~~~~~ initialize ui ~~~~~~~~
    def init_UI(self):
        # set properties
        self.setStyleSheet('QWidget {background-color: #ffffff;}')
        self.setWindowIcon(QIcon('logo.jpg'))
        self.setWindowTitle('Intelligent Know Your Customer')

        # -- welcome image --
        self.welimage = QLabel()
        self.welimage.setMinimumSize(300, 200)
        self.welimage.setAlignment(Qt.AlignCenter)
        self.welimage.setFrameStyle(QFrame.StyledPanel)
        #self.welimage.setStyleSheet('QLabel {background-color: #000000;}')
        imgName = QPixmap('pic1.jpeg')
        self.welimage.setPixmap(imgName)
        self.welimage.setScaledContents(True)

        # -- Login ID label --
        self.name = QLabel('User ID')
        self.name.setFixedHeight(30)
        self.name.setFixedWidth(80)
        self.name.setAlignment(Qt.AlignCenter)
        self.name.setStyleSheet('QLabel {background-color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}')
        
        # -- login userID textbox --
        self.nameinput = QLineEdit()
        self.nameinput.setMinimumSize(150, 30)
        self.nameinput.setStyleSheet('QLineEdit {border: 1px solid #c8c8c8; font-family: ubuntu, arial; font-size: 14px;}')
        

        # -- Login password label --
        self.password = QLabel('Password')
        self.password.setFixedHeight(30)
        self.password.setFixedWidth(80)
        self.password.setAlignment(Qt.AlignCenter)
        self.password.setStyleSheet('QLabel {background-color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}')

        # -- login password textbox --
        self.passwordinput = QLineEdit()
        self.passwordinput.setMinimumSize(150, 30)
        self.passwordinput.setStyleSheet('QLineEdit {border: 1px solid #c8c8c8; font-family: ub/Users/wuqingyi/HKU/COMP/3278/Projectuntu, arial; font-size: 14px;}')
        

        # -- control login button --
        self.btn_login = QPushButton('Log in')
        self.btn_login.setMinimumSize(80, 30)
        self.btn_login_style_0 = 'QPushButton {background-color: #64a0ff; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_login.setStyleSheet(self.btn_login_style_0)
        
        
        # -- control Signup button --
        self.btn_signup = QPushButton('Sign up')
        self.btn_signup.setMinimumSize(100, 30)
        self.btn_signup_style_0 = 'QPushButton {background-color: #64a0ff; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_signup.setStyleSheet(self.btn_signup_style_0)
        
        
        # -- control facelogin button --
        self.btn_facelogin = QPushButton('Face Log In')
        self.btn_facelogin.setMinimumSize(100, 30)
        self.btn_facelogin_style_0 = 'QPushButton {background-color: #64a0ff; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_signup.setStyleSheet(self.btn_facelogin_style_0)
        
        
        # -- cmd window --
        self.cmd_window = QLabel()
        self.cmd_window.setMinimumWidth(100)
        self.cmd_window.setFrameStyle(QFrame.StyledPanel)
        self.cmd_window.setStyleSheet('QLabel {background-color: #000000; color: #ffffff;}')
        
        # -- login message box --
        self.login_message = QPushButton('Close')
        self.login_message.setGeometry(300, 300, 1000,1000)
        
        
        # create layouts
        # create some horizontal box
        h_box_welimage = QHBoxLayout()
        h_box_welimage.addWidget(self.welimage)
        h_box_loginname = QHBoxLayout()
        h_box_loginname.addWidget(self.name)
        h_box_loginname.addWidget(self.nameinput)
        h_box_loginpassword = QHBoxLayout()
        h_box_loginpassword.addWidget(self.password)
        h_box_loginpassword.addWidget(self.passwordinput)
        h_box_loginbtn = QHBoxLayout()
        h_box_loginbtn.addWidget(self.btn_login)
        h_box_loginbtn.addWidget(self.btn_signup)
        h_box_loginbtn.addWidget(self.btn_facelogin)
        h_box_cmd = QHBoxLayout()
        h_box_cmd.addWidget(self.cmd_window)
        

        # create vertical box
        # arrange horizontal boxes vertically
        v_box1 = QVBoxLayout()
        v_box1.addLayout(h_box_welimage)
        
        
        v_box2 = QVBoxLayout()
        v_box2.addLayout(h_box_loginname)
        v_box2.addLayout(h_box_loginpassword)
        v_box2.addLayout(h_box_loginbtn)
        
        v_box3 = QVBoxLayout()
        v_box3.addLayout(h_box_cmd)
        
        v_box4 = QVBoxLayout()
        

        # create grid with boxes created
        g_box0 = QGridLayout()
        g_box0.addLayout(v_box1, 0, 0, 1, 1)
        g_box0.addLayout(v_box2, 2, 0, 2, 2)
        g_box0.addLayout(v_box3, 5, 0, 1, 2)
        g_box0.addLayout(v_box4, 0, 2, -1, 2)

        self.setLayout(g_box0)
        
        
        # connect buttons with functions
        self.btn_login.clicked.connect(self.login)
        self.btn_signup.clicked.connect(self.signup)
        
        return
        
    # ~~~~~~~~ login ~~~~~~~~
    def login(self):
        userID = self.nameinput.text()
        password = self.passwordinput.text()
        sql = "Select * From Login WHERE name = %s AND password = %s"
        input = (userID, password)
        cur.execute(sql, input)
        data = "error"
        for x in cur.fetchall():
            data = x
        if data == "error":
            t1 = "Login failed: The user ID or password is incorrect." ##
            self.cmd_window.setText(t1) ##
            QMessageBox.warning(self, "Warning", "<font size = 5>Login failed<p style='margin:10px'><font size = 3>The user ID or password is incorrect<p style='margin:10px'><font size = 3>Please try again", QMessageBox.Close)
        else:
            sql2 = "Select login_date, login_time From Login WHERE name = %s AND password = %s"
            cur.execute(sql2, input)
            last = cur.fetchone()
            last_date = last[0]
            last_time = last[1]
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M:%S")
            t2 = "Welcome "+str(userID)+"!\nLogin time: "+str(current_date)+" "+str(current_time)+"\nLast Login time: "+str(last_date)+" "+str(last_time) ##
            self.cmd_window.setText(t2) ##
            update =  "UPDATE login SET login_date=%s WHERE name=%s"
            val = (current_date, userID)
            cur.execute(update, val)
            update = "UPDATE login SET login_time=%s WHERE name=%s"
            val = (current_time, userID)
            cur.execute(update, val)
            myconn.commit()


    # ~~~~~~~~ Sign up ~~~~~~~~
    def signup(self):
        dialog = InputDialog()
        if dialog.exec():
            input = dialog.getInputs()
            sql3 = "INSERT INTO login VALUES (%s, %s, %s, %s)"
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M:%S")
            newuser = (input[0], input[1], current_date, current_time)
            cur.execute(sql3, newuser)
            myconn.commit()
            QMessageBox.about(self, "Sign up", "<font size = 5>Sign up successfully!<p style='margin:10px'><font size = 3>Hello %s~ Welcome to iKYC<p style='margin:10px'><font size = 3>Your user ID is: %s<p style='margin:10px'><font size = 3>Please use your user ID to log in" % (input[0],'123')) ##system creates user ID
        
        else:
            QMessageBox.warning(self, "Sign up", "<font size = 5>Sign up failed<p style='margin:10px'><font size = 3>Please try again", QMessageBox.Close)
            t1 = "Sign up failed\nPlease try again" ##
            self.cmd_window.setText(t1) ##


        



# main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    gui = MainGUI()
    gui.show()
    gui.setFixedSize(1100, 600)
    sys.exit(app.exec_())
