import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from model.Database import Database
import view.qrc.login.background_design

class Login(QDialog):
    def __init__(self, widget):
        super(Login, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/login/login.ui"), self)
        self.widget = widget
        self.sqlData = []
        self.session = []

        self.signup_buttn.clicked.connect(self.openSignup)
        self.Login_buttn.clicked.connect(self.login)
    
    def login(self):
        self.sqlData.append(self.email_edit.text())
        self.sqlData.append(self.Password_edit.text())

        if (self.checkCredentials()):
            self.openAccount()
        else:
            print("Please recheck credentials")
    
    def checkCredentials(self):
        sqlStatement = "SELECT * FROM user WHERE school_id = %s AND password = %s"
        db = Database()
        try:
            self.session = list(db.select(sqlStatement, tuple(self.sqlData))[0])
        except Exception as e:
            print(e)
        finally:
            self.sqlData.clear()
        del db

        if self.session:
            return True
        else:
            return False
    
    def openAccount(self):
        if self.session[5] == 1:
            print("Admin account logged in")
        elif self.session[5] == 2:
            print("Teacher account logged in")
        elif self.session[5] == 3:
            print("Student account logged in")
        self.session.clear()
    
    def openSignup(self):
        self.widget.setCurrentIndex(1)
        self.widget.resize(1000, 600)
