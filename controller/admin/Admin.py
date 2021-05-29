import os

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi

from model.Database import Database
from model.Session import Session
from model.ApplicationPage import ApplicationPage
import view.qrc.admin.admin

class Admin(QDialog):
    def __init__(self, widget):
        super(Admin, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/admin/admin.ui"), self)
        self.widget = widget
        self.applicationPage = ApplicationPage()
        
        self.pushButton.clicked.connect(self.loadHomePage)
        self.appoint_2.clicked.connect(self.logoutPage)
        self.next_buttn.clicked.connect(self.nextQueue)
        self.yes_buttn.clicked.connect(self.confirmLogout)
        self.no_buttn.clicked.connect(self.loadHomePage)

        self.loadHomePage()
    
    def nextQueue(self):
        sqlData = []
        sqlData.append(self.currentEnrollee[3])
        sqlStatement = 'UPDATE enrollment SET status = 1 WHERE id = %s'
        
        database = Database()
        try:
            database.save(sqlStatement, tuple(sqlData))
        except Exception as e:
            print(e)
        del database

        self.messageBox('Successful', QMessageBox.Information, 'Next queue will start', QMessageBox.Ok)
        self.loadHomePage()
    
    def loadHomePage(self):
        self.stackedWidget.setCurrentIndex(0)
        self.setHomeEnrollee()
        self.setHomeList()
    
    def setHomeEnrollee(self):
        self.currentEnrollee = self.getCurrentEnrollee()

        try:
            self.queuenumber.setText(self.currentEnrollee[0])
            self.enrollee_name.setText(self.currentEnrollee[1])
            self.course.setText(self.currentEnrollee[2])
        except Exception as e:
            print(e)
            self.queuenumber.setText('None')
            self.enrollee_name.setText('None')
            self.course.setText('None')
    
    def getCurrentEnrollee(self):
        sqlStatement = '''
            SELECT 
                `enrollment`.`queue`,
                `enrollment`.`name`,
                `course`.`name`,
                `enrollment`.`id`
            FROM `enrollment` 
            LEFT JOIN `course` ON `course`.`id` = `enrollment`.`course`
            WHERE
                `enrollment`.`status` = 0
            ORDER BY `enrollment`.`id` ASC LIMIT 1;
        '''

        database = Database()
        try:
            currentEnrollee = database.select(sqlStatement)[0]
        except Exception as e:
            print(e)
        del database

        return currentEnrollee
    
    def setHomeList(self):
        self.list.clear()

        enrollees = self.getItemList()
        
        enrolleeList = []

        for enrollee in enrollees:
            enrolleeList.append(enrollee[0])

        self.list.addItems(enrolleeList)
        self.list.takeItem(0)
    
    def getItemList(self):
        sqlStatement = '''
            SELECT 
                `name`
            FROM `enrollment`
            WHERE
                `status` = 0;
        '''

        database = Database()
        try:
            enrollees = database.select(sqlStatement)
        except Exception as e:
            print(e)
        del database

        return enrollees
    
    def logoutPage(self):
        self.stackedWidget.setCurrentIndex(1)
    
    def confirmLogout(self):
        session = Session()
        try:
            currentUser = session.clearCurrentUser()
        except Exception as e:
            print(e)
        del session

        self.loadHomePage()
        self.widget.setCurrentIndex(self.applicationPage.LOGIN)

    def messageBox(self, title, icon, message, button):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setIcon(icon)
        msg.setText(message)
        msg.setStandardButtons(button)

        returnValue = msg.exec()