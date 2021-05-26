import os

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi

from model.Database import Database
from model.ApplicationPage import ApplicationPage
from model.AccountType import AccountType
import view.qrc.signup.background_design

class Create(QDialog):
    def __init__(self, widget):
        super(Create, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/signup/createaccount.ui"), self)
        self.widget = widget
        self.sqlData_user = []
        self.sqlData_student = []
        self.applicationPage = ApplicationPage()
        self.accountType = AccountType()
        
        self.signup_buttn.clicked.connect(self.signup)
        self.login.clicked.connect(self.openLogin)

        self.loadCourseComboBox()
        self.loadYearComboBox()
    
    def loadCourseComboBox(self):
        sqlStatement = 'SELECT * FROM `course`;'

        items = None
        database = Database()
        try:
            items = database.select(sqlStatement)
        except Exception as e:
            print(e)
        del database
        
        for item in items:
            self.course_box.addItem(item[1], item[0])
    
    def loadYearComboBox(self):
        sqlStatement = 'SELECT * FROM `year_level`;'

        items = None
        database = Database()
        try:
            items = database.select(sqlStatement)
        except Exception as e:
            print(e)
        del database
        
        for item in items:
            self.year_level.addItem(item[1], item[0])
    
    def signup(self):
        errorString = self.checkFields()
        if errorString:
            print(errorString)
        else:
            sqlStatement_user = """
                INSERT INTO `user` (
                    `first_name`, `last_name`, 
                    `school_id`, `password`, `type`
                ) VALUES (%s, %s, %s, %s, %s);
            """

            sqlStatement_student = """
                INSERT INTO `user_student` (
                    `id`, `course`, `year`
                ) VALUES (LAST_INSERT_ID(), %s, %s);
            """

            database = Database()
            try:
                database.save(sqlStatement_user, tuple(self.sqlData_user))
                database.save(sqlStatement_student, tuple(self.sqlData_student))

                self.openLogin()
            except Exception as e:
                print(e)
                print('School ID already exists')
            finally:
                del database
                self.sqlData_user.clear()
                self.sqlData_student.clear()
    
    def clearFields(self):
        self.first_name.setText('')
        self.last_name.setText('')
        self.username_edit_2.setText('')
        self.password_edit.setText('')
        self.course_box.setCurrentIndex(0)
        self.year_level.setCurrentIndex(0)

    def openLogin(self):
        self.clearFields()
        self.widget.setCurrentIndex(self.applicationPage.LOGIN)
        self.widget.resize(1000, 600)
    
    def checkFields(self):
        self.sqlData_user.clear()
        errorString = ''
        if self.first_name.text() != '':
            self.sqlData_user.append(self.first_name.text().title()) # First name
        else:
            errorString += "- First name can't be blank\n"
        
        if self.last_name.text() != '':
            self.sqlData_user.append(self.last_name.text().title()) # Last name
        else:
            errorString += "- Last name can't be blank\n"
        
        if self.username_edit_2.text() != '':
            self.sqlData_user.append(self.username_edit_2.text()) # School ID
        else:
            errorString += "- School ID can't be blank\n"
        
        if self.password_edit.text() != '':
            self.sqlData_user.append(self.password_edit.text()) # Password
        else:
            errorString += "- School ID can't be blank\n"

        self.sqlData_user.append(self.accountType.STUDENT)
        
        if self.course_box.itemData(self.course_box.currentIndex()) != None:
            self.sqlData_student.append(self.course_box.itemData(self.course_box.currentIndex())) # Course
        else:
            errorString += "- Please choose your course\n"

        if self.year_level.itemData(self.year_level.currentIndex()) != None:
            self.sqlData_student.append(self.year_level.itemData(self.year_level.currentIndex())) # Year Level
        else:
            errorString += "- Please choose an your year level\n"

        return errorString
        