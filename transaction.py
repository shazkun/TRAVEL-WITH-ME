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
from authentication import *
from client import *

class TransactionWindow(QDialog):
    def __init__(self, table_widget):
        super(TransactionWindow, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/transaction.ui'
        uic.loadUi(main_ui_path, self)
        self.okbtn.clicked.connect(self.ok_btn)
        self.cancelbtn.clicked.connect(self.hide)
        self.table_widget = table_widget
    
    def ok_btn(self):
        selectedItems = self.table_widget.selectedItems()
        if selectedItems:
            for item in selectedItems:
                item.setText(self.edit_value.text())
        self.hide()