import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTime, QDate

import view.qrc.student.student
from model.Database import Database
from model.Session import Session
from model.ApplicationPage import ApplicationPage

class Student(QDialog):
    def __init__(self, widget):
        super(Student, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/student/student.ui"), self)
        self.widget = widget
        self.pageDashboard = 0
        self.pageAppointment = 1
        self.currentSelectedTeacher = 0
        self.sqlData = []
        self.applicationPage = ApplicationPage()

        self.pushButton.clicked.connect(self.dashboard)
        self.appoint.clicked.connect(self.appointment)
        self.appoint_2.clicked.connect(self.logout)
        self.list.itemClicked.connect(self.selectedItem)
        self.accept_butnn.clicked.connect(self.submitAppointment)
        
        self.loadListWidget()
        self.loadCurrentDateTime()
    
    def loadCurrentDateTime(self):
        self.qt_calendar.setSelectedDate(QDate.currentDate())
        self.timeEdit.setTime(QTime.currentTime())
    
    def getCurrentUser(self):
        session = Session()
        try:
            currentUser = session.currentUser()
        except Exception as e:
            print(e)
        del session

        return currentUser
    
    def submitAppointment(self):
        try:
            self.sqlData.append(self.getCurrentUser()[0][0])
            self.sqlData.append(self.currentSelectedTeacher)
            self.sqlData.append(self.plainTextEdit.toPlainText())
            self.sqlData.append(self.qt_calendar.selectedDate().toString('yyyy-MM-dd') + ' ' + self.timeEdit.time().toString('hh:mm:ss'))

            sqlStatement = "INSERT INTO appointment (`student`, `teacher`, `reason`, `datetime`) VALUES (%s, %s, %s, %s)"
            database = Database()
            try:
                database.save(sqlStatement, tuple(self.sqlData))
            except Exception as e:
                print(self.sqlData)
                print(e)
            del database
            self.sqlData.clear()

        except Exception as e:
            print(e)    
        
        self.loadCurrentDateTime()
        self.plainTextEdit.setPlainText('')
        self.set_3.setText('Faculty')
    
    def selectedItem(self):
        self.set_3.setText(self.list.currentItem().text())
        self.currentSelectedTeacher = self.teacherData[self.list.currentRow()]
    
    def dashboard(self):
        self.stackedWidget.setCurrentIndex(self.pageDashboard)
    
    def appointment(self):
        self.stackedWidget.setCurrentIndex(self.pageAppointment)
    
    def logout(self):
        
        session = Session()
        try:
            currentUser = session.clearCurrentUser()
        except Exception as e:
            print(e)
        del session

        self.dashboard()
        self.widget.setCurrentIndex(self.applicationPage.LOGIN)
    
    def loadListWidget(self):
        self.list.clear()

        sqlString = """
            SELECT
                CONCAT(first_name, ' ', last_name) as name,
                id
            FROM
                user
            WHERE
                type = '1'
                OR type = '2';
        """

        database = Database()
        try:
            listOfTeachers = database.select(sqlString)
        except Exception as e:
            print(e)
        del database
        
        teacherList = []
        self.teacherData = {}

        for index, teacher in enumerate(listOfTeachers):
            teacherList.append(teacher[0])
            self.teacherData[index] = teacher[1]
        
        self.list.addItems(teacherList)
