import os
import datetime

from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

import view.qrc.teacher.teacher
from model.Database import Database
from model.Session import Session
from model.ApplicationPage import ApplicationPage

class Teacher(QDialog):
    def __init__(self, widget):
        super(Teacher, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/teacher/teacher.ui"), self)
        self.applicationPage = ApplicationPage()
        self.widget = widget
        self.currentUser = None
        self.pageDashboard = 0
        self.pageAppointment = 1

        self.pushButton.clicked.connect(self.dashboard)
        self.appoint.clicked.connect(self.appointmentPage)
        self.appoint_2.clicked.connect(self.logout)
        self.listWidget.itemClicked.connect(self.selectedItem)
        self.accept_butnn.clicked.connect(self.acceptAppointment)
        self.decline_buttn.clicked.connect(self.declineAppointment)
    
    def acceptAppointment(self):
        sqlData = []
        
        try:
            sqlData.append(1)
            sqlData.append(self.appointmentData[self.listWidget.currentRow()][5])

            self.updateStatusAppointment(sqlData)
        except Exception as e:
            print(e)
    
    def declineAppointment(self):
        sqlData = []

        try:
            sqlData.append(2)
            sqlData.append(self.appointmentData[self.listWidget.currentRow()][5])

            self.updateStatusAppointment(sqlData)
        except Exception as e:
            print(e)
    
    def updateStatusAppointment(self, sqlData):
        sqlStatement = 'UPDATE appointment SET status = %s WHERE id = %s'

        database = Database()
        try:
            database.save(sqlStatement, tuple(sqlData))
        except Exception as e:
            print(e)
        del database

        self.loadListWidget()
        self.name.setText('Appointee')
        self.yearlevel.setText('Appointee year level')
        self.course.setText('Appointee course')
        self.schoolID.setText('Appointee school ID')

        self.tableWidget.setItem(0, 0, QTableWidgetItem('            '))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('            '))
        self.tableWidget.setItem(0, 2, QTableWidgetItem('            '))
    
    def selectedItem(self):
        self.name.setText(self.listWidget.currentItem().text())
        self.yearlevel.setText((self.appointmentData[self.listWidget.currentRow()])[2])
        self.course.setText(self.appointmentData[self.listWidget.currentRow()][1])
        self.schoolID.setText(self.appointmentData[self.listWidget.currentRow()][0])

        date, time = (self.appointmentData[self.listWidget.currentRow()][3].strftime("%B %d, %Y/%I:%M %p")).split('/')
        itemDate = QTableWidgetItem(date)
        itemDate.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        itemTime = QTableWidgetItem(time)
        itemTime.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        itemReason = QTableWidgetItem(self.appointmentData[self.listWidget.currentRow()][4])
        itemReason.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.tableWidget.setItem(0, 0, itemDate)
        self.tableWidget.setItem(0, 1, itemTime)
        self.tableWidget.setItem(0, 2, itemReason)

        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
    
    def loadListWidget(self):
        self.listWidget.clear()

        sqlString = """
            SELECT
                CONCAT(user.first_name, ' ', user.last_name) AS name,
                appointment.id AS id,
                course.name AS course,
                year_level.year AS year,
                user.school_id AS school_id,
                appointment.datetime AS datetime,
                appointment.reason AS reason
            FROM appointment
            LEFT JOIN user ON user.id = appointment.student
            LEFT JOIN user_student ON user_student.id = appointment.student
            LEFT JOIN course ON course.id = user_student.course
            LEFT JOIN year_level ON year_level.id = user_student.year
            WHERE
                teacher = %s
                AND status = '0';
        """

        database = Database()
        try:
            listOfAppointments = database.select(sqlString, (self.currentUser[0][0],))
        except Exception as e:
            print(e)
        del database
        
        appointmentList = []
        self.appointmentData = {}

        for index, appointment in enumerate(listOfAppointments):
            appointmentList.append(appointment[0])
            self.appointmentData[index] = [appointment[4], appointment[2], appointment[3], appointment[5], appointment[6], appointment[1]]

        self.listWidget.addItems(appointmentList)
        try:
            self.professorsname_4.setText(listOfAppointments[0][0])
            self.prioritynumber_3.setText(str(listOfAppointments[0][1]))
        except Exception as e:
            print(e)
            self.professorsname_4.setText('Appointee')
            self.prioritynumber_3.setText('Appointment ID')
            self.name.setText('Appointee')
            self.yearlevel.setText('Appointee year level')
            self.course.setText('Appointee course')
            self.schoolID.setText('Appointee school ID')

            self.tableWidget.setItem(0, 0, QTableWidgetItem('            '))
            self.tableWidget.setItem(0, 1, QTableWidgetItem('            '))
            self.tableWidget.setItem(0, 2, QTableWidgetItem('            '))
        
    def setProfile(self):
        sqlStatement = """
            SELECT
                CONCAT(first_name, ' ', last_name) AS name,
                id,
                school_id
            FROM user
            WHERE
                id = %s;    
        """

        database = Database()
        try:
            userDetails = database.select(sqlStatement, (self.currentUser[0][0],))[0]
        except Exception as e:
            print(e)
        del database

        self.professorName.setText(userDetails[0])
        self.id.setText(str(userDetails[1]))
        self.gmail.setText(userDetails[2]+'@xu.edu.ph')
    
    def setLatestAppointment(self):
        sqlStatement = """
            SELECT 
                appointment.id AS id,
                CONCAT(student.first_name, ' ', student.last_name) AS student_name
            FROM appointment 
            LEFT JOIN user student ON student.id  = appointment.student
            WHERE 
                appointment.teacher = %s
            ORDER BY appointment.id DESC
            LIMIT 1;
        """
        database = Database()
        try:
            appointmentList = database.select(sqlStatement, (self.currentUser[0][0],))
            self.professorsname_2.setText(appointmentList[0][1])
            self.prioritynumber_2.setText(str(appointmentList[0][0]))
        except Exception as e:
            print(e)
            self.professorsname_2.setText('No latest appointment')
            self.prioritynumber_2.setText('')
        del database

    def getCurrentUser(self):
        session = Session()
        try:
            self.currentUser = session.currentUser()
        except Exception as e:
            print(e)
        del session
    
    def dashboard(self):
        self.stack.setCurrentIndex(self.pageDashboard)
    
    def appointmentPage(self):
        self.stack.setCurrentIndex(self.pageAppointment)

        self.loadListWidget()
    
    def logout(self):
        session = Session()
        try:
            currentUser = session.clearCurrentUser()
        except Exception as e:
            print(e)
        del session

        self.dashboard()
        self.widget.setCurrentIndex(self.applicationPage.LOGIN)