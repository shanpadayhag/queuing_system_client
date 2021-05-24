import os

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi

from model.Database import Database
from model.UserType import convertType

class Create(QDialog):
    def __init__(self, widget):
        super(Create, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/signup/createaccount.ui"), self)
        self.sqlStatement = ""
        self.widget = widget
        self.sqlData = []
        
        self.signup_buttn.clicked.connect(self.signup)
        self.login.clicked.connect(self.openLogin)

        self.loadCourseComboBox()
        self.loadYearComboBox()
    
    def loadCourseComboBox(self):
        self.sqlStatement = 'SELECT * FROM `course`;'

        items = None
        try:
            database = Database()
            items = database.selectAll(self.sqlStatement)
            del database
        except Exception as e:
            print(e)
        
        for item in items:
            self.course_box.addItem(item[1], item[0])
    
    def loadYearComboBox(self):
        self.sqlStatement = 'SELECT * FROM `year_level`;'

        items = None
        try:
            database = Database()
            items = database.selectAll(self.sqlStatement)
            del database
        except Exception as e:
            print(e)
        
        for item in items:
            self.year_level.addItem(item[1], item[0])
    
    def signup(self):
        self.sqlData.append(self.first_name.text()) # First name
        self.sqlData.append(self.last_name.text()) # Last name
        self.sqlData.append(self.username_edit_2.text()) # School ID
        self.sqlData.append(self.password_edit.text()) # Password
        self.sqlData.append(self.course_box.itemData(self.course_box.currentIndex())) # Course
        self.sqlData.append(self.year_level.itemData(self.year_level.currentIndex())) # Year Level
        self.sqlData.append(convertType('student'))
        self.sqlStatement = "INSERT INTO `user` (`first_name`, `last_name`, `school_id`, `password`, `course`, `year`, `type`) VALUES (%s, %s, %s, %s, %s, %s, %s);"

        try:
            database = Database()
            database.insert(self.sqlStatement, tuple(self.sqlData))
            del database

            self.openLogin()
        except Exception as e:
            print(e)
            print('School ID already exists')
        finally:
            self.sqlData.clear()
    
    def clearFields(self):
        self.first_name.setText('')
        self.last_name.setText('')
        self.username_edit_2.setText('')
        self.password_edit.setText('')
        self.course_box.setCurrentIndex(0)
        self.year_level.setCurrentIndex(0)

    def openLogin(self):
        self.clearFields()
        self.widget.setCurrentIndex(0)
        self.widget.resize(1000, 600)
        