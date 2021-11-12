from PyQt5 import QtCore
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QMessageBox, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QToolButton, QFrame
from PyQt5.QtCore import Qt

from datetime import datetime, timedelta
from selectdate import selectdate

class Trans(QWidget):
    def __init__(self, parent, cur, getAccountId) -> None:
        super(Trans, self).__init__(parent)
        self.cur = cur
        self.getAccoutId = getAccountId
        self.init_UI(parent)
        return
    
    
    def init_UI(self, parent):
        # set properties
        self.parent().setWindowTitle("Transaction")
        
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
            if from_date != "" and isinstance(from_date, str) != True:
                from_date = from_date.toString("yyyy-MM-dd")
            global to_date
            if to_date != "" and isinstance(to_date, str) != True:
                to_date = to_date.toString("yyyy-MM-dd")
            

            amount_min_input = amount_Min_input.text()
            amount_max_input = amount_Max_input.text()

            table.clearContents()
            table_show(type, from_time, to_time, from_date, to_date, amount_min_input, amount_max_input)
        
        
        def table_show(type, from_hr_input, to_hr_input, from_date, to_date, amount_min_input, amount_max_input):
            now = datetime.now()
            if amount_min_input == "" :
                amount_min = 0
            else:
                amount_min = amount_min_input
            if amount_max_input == "" :
                amount_max = 999999999
            else:
                amount_max = amount_max_input
            
            if type == "Saving":
                if from_date == "" and to_date == "":
                    delta = timedelta(days=1825)
                    from_date_input = (now - delta).strftime("%Y-%m-%d")
                    to_date_input = (now + delta).strftime("%Y-%m-%d")
                elif from_date != "" and to_date != "":
                    from_date_input = from_date
                    to_date_input = to_date
                elif from_date != "" and to_date == "":
                    from_date_input = from_date
                    delta = timedelta(days=1825)
                    from_date = datetime.strptime(from_date, "%Y-%m-%d")
                    to_date_input = (from_date + delta).strftime("%Y-%m-%d")
                else:
                    to_date_input = to_date
                    delta = timedelta(days=1825)
                    to_date = datetime.strptime(to_date, "%Y-%m-%d")
                    from_date_input = (to_date - delta).strftime("%Y-%m-%d")
                
                sql1 = "Select saving_id, value_date, maturity_date, interest_rate, balance From Saving WHERE account_id = %s AND ((%s <= value_date AND value_date <= %s) OR (%s <= maturity_date AND maturity_date <= %s)) AND %s <= balance AND balance <= %s ORDER BY value_date"
                input = (self.getAccoutId(), from_date_input, to_date_input, now.strftime("%Y-%m-%d"), to_date_input, amount_min, amount_max)
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
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, j, item)

            elif type == "Current":
                if from_hr_input == "" :
                    from_hr_input = "00:00:00"
                if to_hr_input == "":
                    to_hr_input = "23:59:59"
    
                
                if from_date == "" and to_date == "":
                    delta = timedelta(days=30)
                    from_date_input = (now - delta).strftime("%Y-%m-%d")
                    to_date_input = now.strftime("%Y-%m-%d")
                elif from_date != "" and to_date != "":
                    from_date_input = from_date
                    to_date_input = to_date
                elif from_date != "" and to_date == "":
                    from_date_input = from_date
                    to_date_input = now.strftime("%Y-%m-%d")
                else:
                    to_date_input = to_date
                    delta = timedelta(days=30)
                    to_date = datetime.strptime(to_date, "%Y-%m-%d")
                    from_date_input = (to_date - delta).strftime("%Y-%m-%d")
        
                from_datetime = str(from_date_input) + str(from_hr_input)
                to_datetime = str(to_date_input) + str(to_hr_input)
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
                        table.setItem(i, j, item)
                    if data[i][1] == self.getAccoutId():
                        sql2_1 = "Select Customer.name From Account, Customer WHERE Account.customer_id = Customer.customer_id AND Account.account_id = %s" % data[i][2]
                        self.cur.execute(sql2_1)
                        tran_name = self.cur.fetchone()
                        item = QTableWidgetItem()
                        item.setText(str("Transaction to " + tran_name[0] + " " + str(data[i][2])))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, 1, item)
                        item = QTableWidgetItem()
                        item.setText(str(data[i][3]))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, 2, item)
                        item = QTableWidgetItem()
                        item.setText(str(data[i][4]))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, 4, item)
                    else:
                        sql2_2 = "Select Customer.name From Account, Customer WHERE Account.customer_id = Customer.customer_id AND Account.account_id = %s" % data[i][1]
                        self.cur.execute(sql2_2)
                        tran_name = self.cur.fetchone()
                        item = QTableWidgetItem()
                        item.setText(str("Transaction from " + tran_name[0] + " " + str(data[i][1])))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, 1, item)
                        item = QTableWidgetItem()
                        item.setText(str(data[i][3]))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, 3, item)
                        item = QTableWidgetItem()
                        item.setText(str(data[i][6]))
                        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                        table.setItem(i, 4, item)

            else:
                if from_date == "" and to_date == "":
                    delta = timedelta(days=365)
                    from_date_input = (now - delta).strftime("%Y%m")
                    to_date_input = now.strftime("%Y%m")
                elif from_date != "" and to_date != "":
                    from_date = datetime.strptime(from_date, "%Y-%m-%d")
                    from_date_input = from_date.strftime("%Y%m")
                    to_date = datetime.strptime(to_date, "%Y-%m-%d")
                    to_date_input = to_date.strftime("%Y%m")
                elif from_date != "" and to_date == "":
                    from_date = datetime.strptime(from_date, "%Y-%m-%d")
                    from_date_input = from_date.strftime("%Y%m")
                    to_date_input = now.strftime("%Y%m")
                else:
                    to_date = datetime.strptime(to_date, "%Y-%m-%d")
                    to_date_input = to_date.strftime("%Y%m")
                    delta = timedelta(days=365)
                    from_date_input = (to_date - delta).strftime("%Y%m")
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
                        table.setItem(i, j, item)

        # back button
        back_btn = QPushButton(self)
        back_btn.setText("Back")
        back_btn.move(10, 10)
        back_btn.clicked.connect(back)
        
        # Title
        title_label = QLabel(self)
        title_label.setText("Transaction Record")
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
        
        # start date calendar
        def from_cal():
            fromcal = selectdate()
            if fromcal.exec():
                global from_date
                from_date = fromcal.getInputs()
                from_datelbl.setText(from_date.toString(" yyyy-MM-dd"))
    
        # end date calendar
        def to_cal():
            tocal = selectdate()
            if tocal.exec():
                global to_date
                to_date = tocal.getInputs()
                to_datelbl.setText(to_date.toString(" yyyy-MM-dd"))

        
        # from label
        fromlbl = QLabel(self)
        fromlbl.setText('From ')
        fromlbl.setFixedHeight(20)
        fromlbl.move(20, 155)
        
        # from_date input
        from_datelbl = QToolButton(self)
        from_datelbl.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        from_datelbl.setStyleSheet("font-size:13px; border-radius: 10px; border: 2px groove gray; border-style: outset")
        from_datelbl.setText(" Start Date")
        from_datelbl.setArrowType(Qt.DownArrow)
        from_datelbl.setPopupMode(QToolButton.InstantPopup)
        from_datelbl.setAutoRaise(True)
        from_datelbl.setFixedSize(145, 40)
        from_datelbl.move(60, 145)
        global from_date
        from_date = ""
        from_datelbl.clicked.connect(from_cal)
        
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
        
        # to_date input
        to_datelbl = QToolButton(self)
        to_datelbl.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        to_datelbl.setStyleSheet("font-size:13px; border-radius: 10px;  border: 2px groove gray; border-style: outset")
        to_datelbl.setText(" End Date")
        to_datelbl.setArrowType(Qt.DownArrow)
        to_datelbl.setPopupMode(QToolButton.InstantPopup)
        to_datelbl.setAutoRaise(True)
        to_datelbl.setFixedSize(145, 40)
        to_datelbl.move(350, 145)
        global to_date
        to_date = ""
        to_datelbl.clicked.connect(to_cal)

        
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

        return