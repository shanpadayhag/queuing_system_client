import os
from datetime import datetime

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi

from model.Database import Database
from model.ApplicationPage import ApplicationPage
from model.AccountType import AccountType

class Enrollment(QDialog):
    def __init__(self, widget):
        super(Enrollment, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/enrollment/enrollment.ui"), self)
        self.widget = widget
        self.applicationPage = ApplicationPage()
        self.accountType = AccountType()
        self.sqlData = []
        self.course = 0
        self.queueNumber = 0

        self.queueButton.clicked.connect(self.getQueue)
        self.courseCombobox.currentIndexChanged.connect(self.generateNumber)
        self.returnButton.clicked.connect(self.openLogin)

        self.loadCourses()
    
    def openLogin(self):
        self.courseCombobox.setCurrentIndex(0)
        self.nameField.setText('')
        self.queueNumberLabel.setText("Select course")
        self.widget.setCurrentIndex(self.applicationPage.LOGIN)
    
    def generateNumber(self):
        self.course = self.courseCombobox.itemData(self.courseCombobox.currentIndex())

        try:
            self.queueNumberLabel.setText(self.courseDictionary(self.course) + self.getNumber(self.course))
        except Exception as e:
            print(e)
            self.queueNumberLabel.setText("Select course")
    
    def getQueue(self):
        message = self.checkFields()
        if message == '':
            self.sqlData.append(self.queueNumberLabel.text())
            self.sqlData.append(self.nameField.text())
            self.sqlData.append(self.course)
            self.sqlData.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            sqlStatement = "INSERT INTO enrollment (queue, name, course, enrolled_at) VALUES (%s, %s, %s, %s)"

            database = Database()
            try:
                database.save(sqlStatement, tuple(self.sqlData))
                self.incrementCourseNumber(self.course, (self.queueNumber + 1))
            except Exception as e:
                print(e)
            del database

            self.messageBox('Reminder', QMessageBox.Information, 'Please remember your queue number', QMessageBox.Ok)

            self.sqlData.clear()
            self.openLogin()
        else:
            self.messageBox('Warning', QMessageBox.Critical, message, QMessageBox.Ok)

    def loadCourses(self):
        sqlStatement = 'SELECT * FROM `course`;'

        items = None
        database = Database()
        try:
            items = database.select(sqlStatement)
        except Exception as e:
            print(e)
        del database
        
        for item in items:
            self.courseCombobox.addItem(item[1], item[0])
        
    def courseDictionary(self, id):
        course = {
            1: 'CS',
            2: 'EMC',
            3: 'IS',
            4: 'IT',
        }

        return course[id]
    
    def getNumber(self, course):
        sqlStatement = {
            1: 'SELECT `cs` FROM `number`',
            2: 'SELECT `emc` FROM `number`',
            3: 'SELECT `is` FROM `number`',
            4: 'SELECT `it` FROM `number`',
        }

        database = Database()
        try:
            self.queueNumber = database.select(sqlStatement[course])[0][0]
        except Exception as e:
            print(e)
        del database

        return str(self.queueNumber + 1).zfill(3)
    
    def incrementCourseNumber(self, course, newNumber):
        sqlStatement = {
            1: 'UPDATE `number` SET `cs` = %s',
            2: 'UPDATE `number` SET `emc` = %s',
            3: 'UPDATE `number` SET `is` = %s',
            4: 'UPDATE `number` SET `it` = %s',
        }

        database = Database()
        try:
            database.save(sqlStatement[course], (newNumber,))
        except Exception as e:
            print(e)
        del database
    
    def checkFields(self):
        errorString = ""
        if self.courseCombobox.currentIndex() == 0:
            errorString += "- Please choose a course\n"
        if self.nameField.text() == '':
            errorString += "- Please enter your name\n"
        return errorString

    def messageBox(self, title, icon, message, button):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setIcon(icon)
        msg.setText(message)
        msg.setStandardButtons(button)

        returnValue = msg.exec()