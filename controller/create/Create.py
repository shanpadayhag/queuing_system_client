import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class Create(QDialog):
    def __init__(self, widget):
        super(Create, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/signup/createaccount.ui"), self)
        self.widget = widget
        self.login.clicked.connect(self.openLogin)
    
    def openLogin(self):
        self.widget.setCurrentIndex(0)
        self.widget.resize(1000, 600)
        