import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class Admin(QDialog):
    def __init__(self, widget):
        super(Admin, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view/ui/admin/admin.ui"), self)
