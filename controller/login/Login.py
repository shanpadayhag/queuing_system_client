import os

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi

from model.Database import Database
from model.Session import Session
from model.ApplicationPage import ApplicationPage
from model.AccountType import AccountType
import view.qrc.login.background_design

class Login(QDialog):
    def __init__(self, widget, accounts):
        super(Login, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/login/login.ui"), self)
        self.widget = widget
        self.teacherAccount = accounts[1]
        self.studentAccount = accounts[2]
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
            self.messageBox('Congratulations', QMessageBox.Information, 'Logged in successfully', QMessageBox.Ok)
            self.openAccount()
            self.email_edit.setText('')
            self.Password_edit.setText('')
        else:
            self.messageBox('Warning', QMessageBox.Critical, "Email or Password doesn't match or incorrect", QMessageBox.Ok)
    
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

        session = Session()
        try:
            session.clearCurrentUser()
            session.updateCurrentUser(self.session[0])
        except Exception as e:
            print(e)
        del session

        if self.session:
            return True
        else:
            return False
    
    def openAccount(self):
        if self.session[5] == self.accountType.ADMIN:
            self.widget.setCurrentIndex(self.applicationPage.ADMIN)

        elif self.session[5] == self.accountType.TEACHER:
            self.widget.setCurrentIndex(self.applicationPage.TEACHER)
            self.teacherAccount.getCurrentUser()
            self.teacherAccount.setLatestAppointment()
            self.teacherAccount.setProfile()
            self.teacherAccount.loadListWidget()

        elif self.session[5] == self.accountType.STUDENT:
            self.widget.setCurrentIndex(self.applicationPage.STUDENT)
            
        self.session.clear()
    
    def openSignup(self):
        self.widget.setCurrentIndex(self.applicationPage.SIGNUP)
        self.widget.resize(1000, 600)
    
    def openEnrollmentQueue(self):
        self.widget.setCurrentIndex(self.applicationPage.ENROLLMENT)
        self.widget.resize(1000, 600)

    def messageBox(self, title, icon, message, button):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setIcon(icon)
        msg.setText(message)
        msg.setStandardButtons(button)

        returnValue = msg.exec()