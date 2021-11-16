from PyQt5 import QtCore
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QMessageBox, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QFrame, QDateEdit, QDialog, QDialogButtonBox, QFormLayout
from PyQt5.QtCore import Qt

from datetime import datetime, timedelta

class TransferInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        QDialog.setWindowTitle(self, 'Transfer')
        
        global acct, curr, balance
        
        self.from_acct = QLabel(self)
        text = "From         Account " + str(acct)
        self.from_acct.setText(text)
        self.from_acct.setFixedSize(150, 15)
        
        self.from_balance = QLabel(self)
        text = "Balance:   " + str(balance) + "   " + str(curr)
        self.from_balance.setText(text)
        self.from_balance.setFixedSize(150, 20)
        
        self.to_acct = QLineEdit(self)
        self.to_acct.setPlaceholderText("Payee's Account ID")
        self.to_acct.setFixedSize(150, 40)
        
        self.amount = QLineEdit(self)
        self.amount.setPlaceholderText("0.00")
        self.amount.setFixedSize(150, 40)
        
        self.message = QLineEdit(self)
        self.message.setPlaceholderText("optional")
        self.message.setFixedSize(150, 40)
        
        self.noticelbl = QLabel(self)
        self.noticelbl.setText('Notice: Only allow to tranfer between\ncurrent account with same currency')
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        
        layout = QFormLayout(self)
        layout.setLabelAlignment(QtCore.Qt.AlignCenter)
        layout.addRow(self.from_acct)
        layout.addRow(self.from_balance)
        layout.addRow("To", self.to_acct)
        layout.addRow("Amount", self.amount)
        layout.addRow("Message", self.message)
        layout.addRow(self.noticelbl)
        layout.addWidget(buttonBox)
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
    
    def getInputs(self):
        return (self.to_acct.text(), self.amount.text(), self.message.text())

class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.first = QLabel(self)
        self.first.setText("Please enter your password")
        self.second =  PasswordEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        
        layout = QFormLayout(self)
        layout.addRow(self.first)
        layout.addRow(self.second)
        layout.addWidget(buttonBox)
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
    
    def getInputs(self):
        return (self.second.text())

class Trans(QWidget):
    def __init__(self, parent, cur, getAccountId) -> None:
        super(Trans, self).__init__(parent)
        self.cur = cur
        self.getAccoutId = getAccountId
        self.init_UI(parent)
        return
    
    
    def init_UI(self, parent):
        # set properties
        self.parent().setWindowTitle("Account Detail")
        
        now = datetime.now()
        
        def back():
            parent.setLoggedinWigget()
        
        
        def confirm():
            from_hr_input = from_hr.text()
            to_hr_input = to_hr.text()
            if from_hr_input == "" :
                from_hr_input = "00:00"
            if to_hr_input == "":
                to_hr_input = "23:59"
            from_time = from_hr_input + ":" + "00"
            to_time = to_hr_input + ":" + "59"

            try:
                datetime.strptime(from_time, "%H:%M:%S")
            except:
                QMessageBox.warning(self, "Warning", "<font size = 3>Start time fotmat is incorrect<p style='margin:10px'><font size = 3>Please check it and try again", QMessageBox.Close)
            else:
                from_time = from_time
            
            try:
                datetime.strptime(to_time, "%H:%M:%S")
            except:
                QMessageBox.warning(self, "Warning", "<font size = 3>End time fotmat is incorrect<p style='margin:10px'><font size = 3>Please try again", QMessageBox.Close)
            else:
                to_time = to_time

            global from_date
            global to_date

            amount_min_input = amount_Min_input.text()
            amount_max_input = amount_Max_input.text()

            table.clearContents()
            table_show(type, from_time, to_time, from_date, to_date, amount_min_input, amount_max_input)
        
        
        def table_show(type, from_hr_input, to_hr_input, from_date, to_date, amount_min_input, amount_max_input):
            
            if amount_min_input == "" :
                amount_min = 0
            else:
                amount_min = amount_min_input
            if amount_max_input == "" :
                amount_max = 999999999
            else:
                amount_max = amount_max_input
            
            if type == "Saving":
                sql1 = "Select saving_id, value_date, maturity_date, interest_rate, balance From Saving WHERE account_id = %s AND (%s <= value_date AND value_date <= %s) AND %s <= maturity_date AND %s <= balance AND balance <= %s ORDER BY value_date"
                input = (self.getAccoutId(), from_date, to_date, now, amount_min, amount_max)
                self.cur.execute(sql1, input)
                data = self.cur.fetchall()

                table.setColumnCount(5)
                table.setHorizontalHeaderLabels(["Saving ID", "Value Date", "Maturity Date", "Interest Rate (p.a.) %", "Balance"])
                table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                table.setRowCount(len(data))
                table.verticalHeader().hide()
                table.setSelectionBehavior(QAbstractItemView.SelectRows)
                for i in range(len(data)):
                    for j in range(5):
                        item = QTableWidgetItem()
                        item.setText(str(data[i][j]))
                        item.setToolTip(str(data[i][j]))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, j, item)

            elif type == "Current":
                if from_hr_input == "" :
                    from_hr_input = "00:00:00"
                if to_hr_input == "":
                    to_hr_input = "23:59:59"
        
                from_datetime = str(from_date) + str(from_hr_input)
                to_datetime = str(to_date) + str(to_hr_input)
                from_datetime = datetime.strptime(from_datetime, "%Y-%m-%d%H:%M:%S")
                to_datetime = datetime.strptime(to_datetime, "%Y-%m-%d%H:%M:%S")

                sql2 = "Select transac_datetime, from_account, to_account, amount, from_balance, message, to_balance From Transaction WHERE (from_account = %s OR to_account = %s) AND %s <= transac_datetime AND transac_datetime <= %s AND %s <= amount AND amount <= %s ORDER BY transac_datetime"
                input = (self.getAccoutId(), self.getAccoutId(), from_datetime, to_datetime, amount_min, amount_max)
                self.cur.execute(sql2, input)
                data = self.cur.fetchall()

                table.setColumnCount(6)
                table.setHorizontalHeaderLabels(["Transaction Time", "Transaction Details", "Withdraws", "Deposits", "Balance", "Messages"])
                table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                table.setRowCount(len(data))
                table.verticalHeader().hide()
                table.setSelectionBehavior(QAbstractItemView.SelectRows)
                for i in range(len(data)):
                    for j in [0,5]:
                        item = QTableWidgetItem()
                        item.setText(str(data[i][j]))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        item.setToolTip(str(data[i][j]))
                        table.setItem(i, j, item)
                    if data[i][1] == self.getAccoutId():
                        sql2_1 = "Select Customer.name From Account, Customer WHERE Account.customer_id = Customer.customer_id AND Account.account_id = %s" % data[i][2]
                        self.cur.execute(sql2_1)
                        tran_name = self.cur.fetchone()
                        item = QTableWidgetItem()
                        item.setText(str("Transaction to " + tran_name[0] + " " + str(data[i][2])))
                        item.setToolTip(str("Transaction to " + tran_name[0] + " " + str(data[i][2])))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, 1, item)
                        item = QTableWidgetItem()
                        item.setText(str(data[i][3]))
                        item.setToolTip(str(data[i][3]))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, 2, item)
                        item = QTableWidgetItem()
                        item.setText(str(data[i][4]))
                        item.setToolTip(str(data[i][4]))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, 4, item)
                    else:
                        sql2_2 = "Select Customer.name From Account, Customer WHERE Account.customer_id = Customer.customer_id AND Account.account_id = %s" % data[i][1]
                        self.cur.execute(sql2_2)
                        tran_name = self.cur.fetchone()
                        item = QTableWidgetItem()
                        item.setText(str("Transaction from " + tran_name[0] + " " + str(data[i][1])))
                        item.setToolTip(str("Transaction from " + tran_name[0] + " " + str(data[i][1])))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, 1, item)
                        item = QTableWidgetItem()
                        item.setText(str(data[i][3]))
                        item.setToolTip(str(data[i][3]))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, 3, item)
                        item = QTableWidgetItem()
                        item.setText(str(data[i][6]))
                        item.setToolTip(str(data[i][6]))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, 4, item)

            else:
                from_date = datetime.strptime(from_date, "%Y-%m-%d")
                from_date_input = from_date.strftime("%Y%m")
                to_date = datetime.strptime(to_date, "%Y-%m-%d")
                to_date_input = to_date.strftime("%Y%m")

                from_month = int(from_date_input)
                to_month = int(to_date_input)

                sql3 = "Select month, bill, due_date, repay_date From Credit WHERE account_id = %s AND %s <= month AND month <= %s AND %s <= bill AND bill <= %s ORDER BY month DESC"
                input = (self.getAccoutId(), from_month, to_month, amount_min, amount_max)
                self.cur.execute(sql3, input)
                data = self.cur.fetchall()

                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Month", "Balance", "Due Date", "Repay Date"])
                table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                table.setRowCount(len(data))
                table.verticalHeader().hide()
                table.setSelectionBehavior(QAbstractItemView.SelectRows)
                for i in range(len(data)):
                    for j in range(4):
                        item = QTableWidgetItem()
                        item.setText(str(data[i][j]))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        item.setToolTip(str(data[i][j]))
                        table.setItem(i, j, item)

        # back button
        back_btn = QPushButton(self)
        back_btn.setText("Back")
        back_btn.move(10, 10)
        back_btn.clicked.connect(back)
        
        # Title
        title_label = QLabel(self)
        title_label.setText("Account Detail")
        title_label.setStyleSheet("font-size:22px;font-weight:bold;")
        title_label.move(10, 60)
        
        # display username
        name_label = QLabel(self)
        sql = "Select name From Account A, Customer C WHERE A.customer_id = C.customer_id AND account_id = %s" % (self.getAccoutId())
        self.cur.execute(sql)
        output = self.cur.fetchone()
        cname = output[0]
        name_label.setText("Username: " + cname)
        name_label.setStyleSheet("font-size:15px;")
        name_label.move(10, 100)
        
        # display Account type&ID
        sql1 = "Select type, currency From Account WHERE account_id = %s" % (self.getAccoutId())
        self.cur.execute(sql1)
        output = self.cur.fetchone()
        type = output[0]
        currency = output[1]
        acc_label = QLabel(self)
        acc_label.setText("Account Number: " + str(currency) + " " + str(type) + " Account " + str(self.getAccoutId()))
        acc_label.setStyleSheet("font-size:15px;")
        acc_label.move(200, 100)

        
        # Hline
        line = QFrame(self)
        line.setLineWidth(3)
        #line.setMidLineWidth(2)
        line.setFrameShadow(QFrame.Sunken)
        line.setGeometry(QtCore.QRect(5, 127, 450, 8))
        line.setStyleSheet("background-color: lightgrey; border: 2px groove gray ; border-style: outset")
        line.setFrameShape(QFrame.HLine)

        
        # from label
        fromlbl = QLabel(self)
        fromlbl.setText('From ')
        fromlbl.setFixedHeight(20)
        fromlbl.move(20, 155)
        
        
        def fromDateChange():
            global from_date
            from_date = self.from_dateEdit.date().toString("yyyy-MM-dd")
        
        def toDateChange():
            global from_date
            to_date = self.to_dateEdit.date().toString("yyyy-MM-dd")
        
        global from_date
        from_date = ""
        global to_date
        to_date = ""
        
        # from_date/to_date input
        def dateSelection(type, from_date, to_date):
            if type == "Saving":
                delta1 = now - timedelta(days=1095)
                self.from_dateEdit = QDateEdit(delta1, self)
                self.to_dateEdit = QDateEdit(now, self)
            
            elif type == "Current":
                delta1 = now - timedelta(days=30)
                self.from_dateEdit = QDateEdit(delta1, self)
                self.to_dateEdit = QDateEdit(now, self)
            
            else:
                delta1 = now - timedelta(days=180)
                self.from_dateEdit = QDateEdit(delta1, self)
                self.to_dateEdit = QDateEdit(now, self)

        dateSelection(type, from_date, to_date)

        self.from_dateEdit.setDisplayFormat('yyyy-MM-dd')
        self.from_dateEdit.setCalendarPopup(True)
        self.from_dateEdit.setFixedSize(145, 40)
        self.from_dateEdit.move(60, 145)
        from_date = self.from_dateEdit.date().toString("yyyy-MM-dd")
        self.from_dateEdit.dateChanged.connect(fromDateChange)

        self.to_dateEdit.setDisplayFormat('yyyy-MM-dd')
        self.to_dateEdit.setCalendarPopup(True)
        self.to_dateEdit.setFixedSize(145, 40)
        self.to_dateEdit.move(350, 145)
        to_date = self.to_dateEdit.date().toString("yyyy-MM-dd")
        self.to_dateEdit.dateChanged.connect(toDateChange)
    

        # from_time_hour input
        from_hr = QLineEdit(self)
        from_hr.setFixedSize(100, 33)
        from_hr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        from_hr.setPlaceholderText("e.g. 08:08")
        from_hr.move(215, 148)
        from_hr_input = ""
        
        # to label
        tolbl = QLabel(self)
        tolbl.setText('To ')
        tolbl.setFixedHeight(20)
        tolbl.move(325, 155)
        
        # to_time_hour input
        to_hr = QLineEdit(self)
        to_hr.setFixedSize(100, 33)
        to_hr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        to_hr.move(505, 148)
        to_hr_input = ""
        
        # to label
        timelbl = QLabel(self)
        timelbl.setText('Time format: 24-hour clock')
        timelbl.setFixedHeight(20)
        timelbl.move(615, 155)


        # amount label
        amount = QLabel(self)
        amount.setText('Amount')
        amount.setFixedHeight(20)
        amount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amount.move(20, 210)
        
        # amount_Min input
        amount_Min_input = QLineEdit(self)
        amount_Min_input.setFixedSize(90, 30)
        amount_Min_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amount_Min_input.setPlaceholderText("Min")
        amount_Min_input.move(75, 205)
        amount_min_input = ""
        
        # amount label
        amount = QLabel(self)
        amount.setText('~')
        amount.setStyleSheet("font-size:10px;font-weight:bold;")
        amount.setFixedHeight(20)
        amount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amount.move(170, 210)
        
        # amount_Max input
        amount_Max_input = QLineEdit(self)
        amount_Max_input.setFixedSize(90, 30)
        amount_Max_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amount_Max_input.setPlaceholderText("Max")
        amount_Max_input.move(183, 205)
        amount_max_input = ""
        
        # search label
        search = QLabel(self)
        search.setText('Enter your request to search for specified records')
        search.setFixedHeight(20)
        search.move(320, 210)

       
        # confirm button
        confirm_btn = QPushButton(self)
        confirm_btn.setText("SUBMIT")
        confirm_btn.move(610, 198)
        confirm_btn.clicked.connect(confirm)
        
        # Setup Table
        table = QTableWidget(self)
        table.move(20, 270)
        table.resize(1200, 410)
        table_show(type, from_hr_input, to_hr_input, from_date, to_date, amount_min_input, amount_max_input)

        def transfer():
            from_acct = TransferInputDialog()
            if from_acct.exec():
                input = from_acct.getInputs()
                to_input = input[0]
                amount_input = input[1]
                message_input = input[2]
                sql1 = "SELECT A.account_id, A.currency, CU.balance FROM account A, current CU WHERE A.account_id = %s AND A.account_id = CU.account_id" %self.getAccoutId()
                self.cur.execute(sql1)
                data1 = self.cur.fetchone()
                from_acct = data1[0]
                from_cur = data1[1]
                from_balance = data1[2]
                if to_input == "":
                    QMessageBox.warning(self, "Warning", "<font size = 4>Please input Payee's Account ID", QMessageBox.Close)
                elif amount_input == "":
                    QMessageBox.warning(self, "Warning", "<font size = 4>Please input transfer amount", QMessageBox.Close)
                elif to_input.isdigit() == False:
                    QMessageBox.warning(self, "Warning", "<font size = 4>Payee's Account ID should be a number. Please input correct Payee's Account ID", QMessageBox.Close)
                elif amount_input.isdigit() == False:
                    QMessageBox.warning(self, "Warning", "<font size = 4>Transfer amount should be a number. Please input correct transfer amount", QMessageBox.Close)
                elif int(amount_input) <= 0:
                    QMessageBox.warning(self, "Warning", "<font size = 4>Please input positive transfer amount", QMessageBox.Close)
                elif from_balance < int(amount_input):
                    QMessageBox.warning(self, "Warning", "<font size = 4>Transfer amount exceed your current account balance<p style='margin:10px'><font size = 3>Please try again", QMessageBox.Close)
                else:
                    sql2 = "SELECT A.account_id, A.type, A.currency, CU.balance FROM account A, current CU WHERE A.account_id = %s AND A.account_id = CU.account_id" % to_input
                    self.cur.execute(sql2)
                    data2 = self.cur.fetchone()
                    if data2 == None:
                        QMessageBox.warning(self, "Warning", "<font size = 5>Payee's Account ID is incorrect or not a current account<p style='margin:10px'><font size = 3>Please check it and try again", QMessageBox.Close)
                    else:
                        to_acct = data2[0]
                        to_curr = data2[2]
                        to_balance = data2[3]
                        if to_curr != from_cur:
                            QMessageBox.warning(self, "Warning", "<font size = 5>Payee's Account Curreny type is not same<p style='margin:10px'><font size = 3>Please check it and try again", QMessageBox.Close)
                        elif from_acct == to_acct:
                            QMessageBox.warning(self, "Warning", "<font size = 5>Cannot transfer to your same account<p style='margin:10px'><font size = 3>Please check it and try again", QMessageBox.Close)
                        else:
                            pwd = PasswordDialog()
                            if pwd.exec():
                                password = pwd.getInputs()
                                sql = "SELECT A.account_id FROM account A, Customer C WHERE A.account_id = %s AND C.password = SHA2(%s, 224) AND A.customer_id = C.customer_id"
                                input = (self.getAccoutId(), password)
                                self.cur.execute(sql, input)
                                result = self.cur.fetchone()
                                if result:
                                    from_balance_after = float(from_balance) - float(amount_input)
                                    to_balance_after = float(to_balance) + float(amount_input)
                                    update1 =  "UPDATE Current SET balance=%s WHERE account_id=%s"
                                    val = (from_balance_after, from_acct)
                                    self.cur.execute(update1, val)
                                    update2 =  "UPDATE Current SET balance=%s WHERE account_id=%s"
                                    val = (to_balance_after, to_acct)
                                    self.cur.execute(update2, val)
                                    update3 =  "INSERT INTO Transaction VALUES (null, %s, %s, %s, %s, %s, %s, %s)"
                                    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
                                    val = (from_acct, to_acct, float(amount_input), current_datetime, from_balance_after, to_balance_after, message_input)
                                    self.cur.execute(update3, val)
                                    QMessageBox.about(self, "Transfer Successfully", "<font size = 5>Your transfer transaction is completed<p style='margin:10px'><font size = 3>Please refresh the page by press SUBMIT button to see latest transaction")
                                else:
                                    QMessageBox.warning(self, "Warning", "<font size = 5>Password Incorrect!<p><font size = 3>Please check your password", QMessageBox.Close)
        


        
        # transfer button
        if type == "Current":
            transfer_btn = QPushButton(self)
            transfer_btn.setText("Transfer")
            transfer_btn.move(1100, 198)
            sql1 = "SELECT A.account_id, A.currency, CU.balance FROM Account A, Current CU WHERE A.account_id = %s AND A.account_id = CU.account_id" % (self.getAccoutId())
            self.cur.execute(sql1)
            output = self.cur.fetchone()
            global acct, curr, balance
            acct = output[0]
            curr = output[1]
            balance = output[2]
            transfer_btn.clicked.connect(transfer)
        
        
        return

