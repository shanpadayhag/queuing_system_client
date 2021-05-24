import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class Login(QDialog):
    def __init__(self, widget):
        super(Login, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/login/login.ui"), self)
        self.widget = widget
        self.signup_buttn.clicked.connect(self.openSignup)
    
    def openSignup(self):
        self.widget.setCurrentIndex(1)
        self.widget.resize(1000, 600)