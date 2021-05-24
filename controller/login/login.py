import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/login/login.ui"), self)


# import sys, database as db
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem
# from PyQt5.uic import loadUi
# from datetime import datetime

# class choose_ui(QDialog):
#     def __init__(self):
#         super(choose_ui,self).__init__()
#         loadUi("ui/choose_ui.ui",self)
#         self.admin_bttn.clicked.connect(self.open_prio_num)
#         self.faculty_buttn.clicked.connect(self.open_faculty_login)
#         self.student_bttn.clicked.connect(self.open_student_login)
#         self.closebuttn.clicked.connect(self.close_window)
#         widget.setFixedSize(643,680)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     widget = QtWidgets.QStackedWidget()

#     Choose_UI = choose_ui()
#     widget.addWidget(Choose_UI)
#     widget.setCurrentIndex(widget.currentIndex() + 1)
#     widget.setWindowTitle("Queuing System")
#     widget.show()
#     app.exec_()
