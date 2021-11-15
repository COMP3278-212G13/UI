from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QMessageBox, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QWidget
from PyQt5.QtGui import QPixmap


class ProfileWidget(QWidget):
    def __init__(self, parent, cur, getUserId, setAccountId, getLastTime):
        super(ProfileWidget, self).__init__(parent)
        self.cur = cur
        self.getUserId = getUserId
        self.setAccountId = setAccountId
        self.getLastTime = getLastTime
        self.init_window(parent)
    
    def init_window(self, parent):
        userid = self.getUserId()
        sql = "SELECT name, login_date, login_time FROM customer WHERE customer_id = " + userid
        self.cur.execute(sql)
        row = self.cur.fetchone()
        cname = row[0]
        current_date = str(row[1])
        current_time = str(row[2])
        
        # window title
        self.parent().setWindowTitle("Profile Overview--" + cname)
        
        def logout():
            reply = QMessageBox.information(self, "Logout", "Are you sure to log out?", QMessageBox.Yes | QMessageBox.No) == 16384
            if reply:
                parent.setLoggedout()

        # logout button
        logout_btn = QPushButton(self)
        logout_btn.setText("logout")
        logout_btn.move(1199, 0)
        logout_btn.clicked.connect(logout)
        
        # image
        pix = QPixmap('assets/Title1.png')
        img_lbl = QLabel(self)
        img_lbl.setPixmap(pix)
        img_lbl.move(0, 0)
        img_lbl.setMinimumSize(200, 30)
        img_lbl.setScaledContents(True)
        
        # display username
        name_label = QLabel(self)
        name_label.setText("Username: " + cname)
        name_label.move(20, 90)

        # display last login time
        login_label = QLabel(self)
        login_label.setText("Last login: " + str(self.getLastTime()[0]) + " " + str(self.getLastTime()[1]))
        login_label.move(220, 90)
        
        # display current login time
        cur_lbl = QLabel(self)
        cur_lbl.setText("Current login: " + current_date + " " + current_time)
        cur_lbl.move(480, 90)

        # accounts title
        acct_label = QLabel(self)
        acct_label.setText("Your Accounts:    Double click to check account details")
        acct_label.move(20, 120)

        # table of accounts
        sql = '''
            SELECT *
            FROM (
                SELECT account_id, type, currency, balance_or_bill
		        FROM(
		            SELECT A.account_id AS account_id, A.type AS type, A.currency AS currency, CR.bill AS balance_or_bill
                    FROM account A, credit CR
                    WHERE (
                        A.customer_id = %s
	                    AND A.account_id = CR.account_id
                    ) ORDER BY CR.month DESC limit 1
		            ) AS temp
		        ) AS temp1 UNION (
		        SELECT A.account_id AS account_id, A.type AS type, A.currency AS currency, SUM(CU.balance) AS balance_or_bill
		        FROM account A, current CU
		        WHERE (
	                A.customer_id = %s
				    AND A.account_id = CU.account_id
		        ) GROUP BY account_id
		        )  UNION (
		        SELECT A.account_id AS account_id, A.type AS type, A.currency AS currency, SUM(S.balance) AS balance_or_bill
		        FROM account A, saving S
		        WHERE (
	                A.customer_id = %s
				    AND A.account_id = S.account_id
	            ) GROUP BY account_id
		    ) ORDER BY account_id'''
        input = (userid, userid, userid)
        self.cur.execute(sql, input)
        data = ()
        data = self.cur.fetchall()

        def dc_handle(row, col):
            self.setAccountId(data[row][0])
            parent.setAccountWidget()

        if data:
            table = QTableWidget(self)
            table.resize(1200, 400)
            table.setColumnCount(4)
            table.setRowCount(len(data))
            table.setHorizontalHeaderLabels(["Account ID", "Account Type", "Currency", "Balance/Bill"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            #table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.setSelectionBehavior(QAbstractItemView.SelectRows)
            for i in range(len(data)):
                for j in range(4):
                    item = QTableWidgetItem()
                    if (j == 3):
                        item.setText(str(format(data[i][j], '.1f')))
                    else:
                        item.setText(str(data[i][j]))
                    table.setItem(i, j, item)
            table.move(30, 160)
            table.verticalHeader().setVisible(False)
            table.cellDoubleClicked[int, int].connect(dc_handle)
        else:
            nf_label = QLabel(self)
            nf_label.setText("Sorry! You have no account!")
            nf_label.move(0, 120)
