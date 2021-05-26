import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class Student(QDialog):
    def __init__(self, widget):
        super(Student, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/student/student.ui"), self)
