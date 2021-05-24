import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget

from controller.login.Login import Login
from controller.create.Create import Create


class Handler:
    def __init__(self):
        app = QApplication(sys.argv)
        self.widget = QStackedWidget()

        self.loadInterfaces()

        self.widget.setCurrentIndex(0)
        self.widget.resize(1000, 600)

        self.widget.setWindowTitle("Queuing System")
        self.widget.show()
        app.exec_()

    def loadInterfaces(self):
        login = Login(self.widget)
        signup = Create(self.widget)

        models = [login, signup]

        self.addInterfaces(models)

    def addInterfaces(self, models):
        for model in models:
            self.widget.addWidget(model)
