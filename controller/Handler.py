import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget

from controller.login.Login import Login
from controller.create.Create import Create
from controller.admin.Admin import Admin
from controller.student.Student import Student
from controller.teacher.Teacher import Teacher
from controller.enrollment.Enrollment import Enrollment
from model.ApplicationPage import ApplicationPage


class Handler:
    def __init__(self):
        app = QApplication(sys.argv)
        self.widget = QStackedWidget()

        self.loadInterfaces()

        self.widget.setCurrentIndex(ApplicationPage().LOGIN)
        self.widget.resize(1000, 600)

        self.widget.setWindowTitle("Queuing System")
        self.widget.show()
        app.exec_()

    def loadInterfaces(self):
        login = Login(self.widget)
        signup = Create(self.widget)
        enrollment = Enrollment(self.widget)
        admin = Admin(self.widget)
        teacher = Teacher(self.widget)
        student = Student(self.widget)

        models = [login, signup, enrollment, admin, teacher, student]

        self.addInterfaces(models)

    def addInterfaces(self, models):
        for model in models:
            self.widget.addWidget(model)
