import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget

from controller.login.Login import Login


class Handler:
    def __init__(self):
        app = QApplication(sys.argv)
        self.widget = QStackedWidget()

        self.loadInterfaces()

        self.widgetPageSetTo('login')
        self.widget.setWindowTitle("Queuing System")
        self.widget.show()
        app.exec_()

    def widgetPageSetTo(self, page):
        # Dictionary {<name of page>: <index> <width> <height>}
        pages = {
            'login': '0 1000 594'
        }

        pageConfig = pages.get(page)
        pageConfig = [int(page) for page in pageConfig.split()]
        self.widgetPageConfig(pageConfig[0], pageConfig[1], pageConfig[2])

    def widgetPageConfig(self, index, width, height):
        self.widget.setCurrentIndex(index)
        self.widget.resize(width, height)

    def loadInterfaces(self):
        login = Login()

        models = [login]

        self.addInterfaces(models)

    def addInterfaces(self, models):
        for model in models:
            self.widget.addWidget(model)


# app = QApplication(sys.argv)
#     widget = QStackedWidget()

#     # ADDING THE MAIN WINDOW UI TO STACKED WIDGET
#     MainWindow = MainWindow()
#     widget.addWidget(MainWindow)

#     # ADDING THE SENT EMAIL LISTS WINDOW UI TO STACKED WIDGET
#     SentEmailListWindow = SentEmailListWindow()
#     widget.addWidget(SentEmailListWindow)

#     # SETTING THE CURRENT WIDGET TO MAIN WINDOW UI
#     widget.setCurrentIndex(0)
#     widget.resize(410, 650)

#     # SETTING UP THE APPLICATION ICON, WINDOW TITLE, THEN SHOW ON SCREEN
#     widget.setWindowIcon(QIcon('favicon.png'))
#     widget.setWindowTitle("Simple Email Sender")
#     widget.show()
#     app.exec_()
