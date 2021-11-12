from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QMessageBox, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QWidget


class ProfileWidget(QWidget):
    def __init__(self, parent, cur, getUserId, setAccountId):
        super(ProfileWidget, self).__init__(parent)
        self.cur = cur
        self.getUserId = getUserId
        self.setAccountId = setAccountId
        self.init_window(parent)
    
    def init_window(self, parent):
        userid = self.getUserId()
        sql = "SELECT name, login_date, login_time FROM customer WHERE customer_id = " + userid
        self.cur.execute(sql)
        row = self.cur.fetchone()
        cname = row[0]
        last_date = str(row[1])
        last_time = str(row[2])
        
        # window title
        self.parent().setWindowTitle("Profile Overview--" + cname)
        # self.parent().resize(400, 600)
        # self.parent().move(0, 0)
        
        def logout():
            reply = QMessageBox.information(self, "Logout", "Are you sure to log out?", QMessageBox.Yes | QMessageBox.No) == 16384
            if reply:
                parent.setLoggedout()

        # logout button
        logout_btn = QPushButton(self)
        logout_btn.setText("logout")
        logout_btn.move(1000, 0)
        logout_btn.clicked.connect(logout)
        
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
        self.cur.execute(sql, input)
        data = ()
        data = self.cur.fetchall()

        def dc_handle(row, col):
            self.setAccountId(data[row][0])
            parent.setAccountWidget()

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
            table.cellDoubleClicked[int, int].connect(dc_handle)
        else:
            nf_label = QLabel(self)
            nf_label.setText("Sorry! You have no account!")
            nf_label.move(0, 100)
