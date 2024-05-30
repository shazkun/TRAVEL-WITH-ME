from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget
from prompts import * 
import sys
import icons.resources_rc
from database import *
import authentication
from packages import *
import time




class StartWindow(QMainWindow, BaseWindow):
    def __init__(self):
        super(StartWindow, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/start.ui'
        uic.loadUi(main_ui_path, self)
        self.start.clicked.connect(self.openauth)
        self.progressBar.setValue(0)  # Start with 0% progress
        self.start.hide()
        self.progress_value = 30
        self.timer = QTimer(self)
        self.progressBar.setTextVisible(False)
        self.timer.timeout.connect(self.increment_progress)
        self.timer.start(100)  # Adjust the interval for progress increment speed

    def increment_progress(self):
        self.progress_value += 10
        if self.progress_value > 100:
            self.progressBar.hide()
            self.start.show()
        self.progressBar.setValue(self.progress_value)
        


    def openauth(self):
        self.hide()
        self.main = authentication.AuthWindow()
        if self.isMaximized():
            self.main.showMaximized()
        self.main.show()
