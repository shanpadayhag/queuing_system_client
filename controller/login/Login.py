import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from model.Database import Database
from model.ApplicationPage import ApplicationPage
from model.AccountType import AccountType
import view.qrc.login.background_design

class Login(QDialog):
    def __init__(self, widget):
        super(Login, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/login/login.ui"), self)
        self.widget = widget
        self.sqlData = []
        self.session = []
        self.applicationPage = ApplicationPage()
        self.accountType = AccountType()

        self.signup_buttn.clicked.connect(self.openSignup)
        self.Login_buttn.clicked.connect(self.login)
        self.Queue_buttn.clicked.connect(self.openEnrollmentQueue)
    
    def login(self):
        self.sqlData.append(self.email_edit.text())
        self.sqlData.append(self.Password_edit.text())

        if (self.checkCredentials()):
            self.openAccount()
        else:
            print("Please recheck credentials")
    
    def checkCredentials(self):
        sqlStatement = "SELECT * FROM user WHERE school_id = %s AND password = %s"
        database = Database()
        try:
            self.session = list(database.select(sqlStatement, tuple(self.sqlData))[0])
        except Exception as e:
            print(e)
        finally:
            self.sqlData.clear()
        del database

        if self.session:
            return True
        else:
            return False
    
    def openAccount(self):
        if self.session[5] == self.accountType.ADMIN:
            self.widget.setCurrentIndex(self.applicationPage.ADMIN)

        elif self.session[5] == self.accountType.TEACHER:
            self.widget.setCurrentIndex(self.applicationPage.TEACHER)

        elif self.session[5] == self.accountType.STUDENT:
            self.widget.setCurrentIndex(self.applicationPage.STUDENT)
            
        self.session.clear()
    
    def openSignup(self):
        self.widget.setCurrentIndex(self.applicationPage.SIGNUP)
        self.widget.resize(1000, 600)
    
    def openEnrollmentQueue(self):
        self.widget.setCurrentIndex(self.applicationPage.ENROLLMENT)
        self.widget.resize(1000, 600)
