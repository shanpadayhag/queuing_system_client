import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class Teacher(QDialog):
    def __init__(self, widget):
        super(Teacher, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/teacher/teacher.ui"), self)
