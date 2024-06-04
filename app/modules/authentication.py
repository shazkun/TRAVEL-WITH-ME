from PyQt5.QtWidgets import *
from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from modules.prompts import *
import sys
import modules.icons.resources_rc
from modules.database import *
from modules.menu import Main

class AuthWindow(QMainWindow, BaseWindow):
    def __init__(self):
        super(AuthWindow, self).__init__()
        self.db = DatabaseHandler()
        self.init_ui()

    def init_ui(self):
        main_ui_path = Path(__file__).resolve().parent / 'ui/auth.ui'
        uic.loadUi(main_ui_path, self)
        self.loginb.clicked.connect(self.login)

        self.L1.clicked.connect(self.login1)
        self.R1.clicked.connect(self.register1)
        self.L2.clicked.connect(self.login1)
        self.R2.clicked.connect(self.register1)
        #LABEL TEXT CHANGE WINDOW
        self.cabtn.clicked.connect(self.register1)
        self.albtn.clicked.connect(self.login1)

        self.registerbtn.clicked.connect(self.register)
    
       
    def openmain(self, user_id ):
        self.main = Main(user_id)
        self.hide()
        if self.isMaximized():
            self.main.showMaximized()
        self.main.show()
    


    def login1(self):
        self.stackedWidget.setCurrentWidget(self.stackedWidget.findChild(QWidget, "loginpage"))
    def register1(self):
        self.stackedWidget.setCurrentWidget(self.stackedWidget.findChild(QWidget, "registerpage"))
    def login(self):
        username = self.username.text().lower()
        password = self.password.text()

        user_id = self.db.login_user(username, password)
        if user_id:
            self.openmain(user_id)
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password')

    def register(self):
        username = self.register_username.text().lower()
        password = self.register_password.text()
        confirm_password = self.confirm_password.text()

        if len(username) < 4:
            QMessageBox.warning(self, 'Registration Failed', 'Username must be at least 4 characters long.')
            return
        if len(password) < 8:
            QMessageBox.warning(self, 'Registration Failed', 'Password must be at least 8 characters long.')
            return

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, 'Registration Failed', 'All fields are required')
            return

        if password != confirm_password:
            QMessageBox.warning(self, 'Registration Failed', 'Passwords do not match')
            return

        success = self.db.register_user(username, password)
        if success:
            self.register_success()
        else:
            QMessageBox.warning(self, 'Registration Failed', 'Username already exists')
    def register_success(self):
        dialog = SuccessPrompt()
        if dialog.exec_() == QDialog.Accepted:
            self.login1()
        else:
            pass
       
            
    def setBackground(self, user_id):
        getvalue = self.db.get_bg(user_id)
        if getvalue == True:
            with open(str(Path(__file__).resolve().parent /"css/auth_dark.css"), "r") as file:
                self.setStyleSheet(file.read())
           
        if getvalue == False:
            with open(str(Path(__file__).resolve().parent /"css/auth_light.css"), "r") as file:
                self.setStyleSheet(file.read())
        
