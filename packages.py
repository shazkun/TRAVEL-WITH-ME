from PyQt5.QtWidgets import *
from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from prompts import *
import sys
import icons.resources_rc
from database import *
import authentication
from client import ClientWindow
from transaction import TransactionWindow


class PackageWindow(QDialog):
    def __init__(self):
        super(PackageWindow, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/package.ui'
        uic.loadUi(main_ui_path, self)
        self.okbtn.clicked.connect(self.ok_btn)
    
    def ok_btn(self):
        self.hide()


class LogsWindow(QDialog):
    def __init__(self):
        super(LogsWindow, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/logs.ui'
        uic.loadUi(main_ui_path, self)
        self.okbtn.clicked.connect(self.ok_btn)
    
    def ok_btn(self):
        self.hide()
