from PyQt5.QtWidgets import *
from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
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
    def __init__(self, db, user_id):
        super(PackageWindow, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/package.ui'
        uic.loadUi(main_ui_path, self)
        self.db = db
        self.user_id = user_id
        self.table_widget = self.findChild(QTableWidget, 'tableWidget')
        self.okbtn.clicked.connect(self.ok_btn)
        self.addbtn.clicked.connect(self.add_package)
        # self.editbtn.clicked.connect(self.update_package)
        self.delbtn.clicked.connect(self.delete_package)
        self.table_flags()
        self.load_packages()

    def table_flags(self):
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setColumnHidden(0, True)

    def ok_btn(self):
        self.hide()

    def load_packages(self):
        self.table_widget.setRowCount(0)  # Clear existing rows
        clients = self.db.fetch_user_packages(self.user_id)
        for client in clients:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            for col, data in enumerate(client):
                self.table_widget.setItem(
                    row_position, col, QTableWidgetItem(str(data)))

    def add_package(self):
        self.main = PackageAddPrompt()
        if self.main.exec_() == QDialog.Accepted:
            i = self.main.load()
            self.db.insert_package(self.user_id, i[0], i[1], i[2])
            self.load_packages()

    # def update_package(self):
    #     selected_items = self.tableWidget.selectedItems()
    #     if not selected_items:
    #         QMessageBox.warning(self, 'No Selection', 'Please select an item to update.')
    #         return

    #     selected_row = self.tableWidget.currentRow()
    #     package_id = int(self.tableWidget.item(selected_row, 0).text())  # Assuming the first column is the package ID
    #     package_type = self.packageTypeLineEdit.text()
    #     destination = self.destinationLineEdit.text()
    #     cost = float(self.costLineEdit.text())
    #     self.db.update_package(package_id, package_type, destination, cost)
    #     self.load_packages()

    def delete_package(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'No Selection',
                                'Please select an item to delete.')
            return

        selected_row = self.table_widget.currentRow()
        # Assuming the first column is the package ID
        package_id = self.table_widget.item(selected_row, 0).text()
        self.db.delete_package(package_id)
        self.load_packages()


class PackageAddPrompt(QDialog):
    def __init__(self):
        super(PackageAddPrompt, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/p_forms.ui'
        uic.loadUi(main_ui_path, self)
        self.savebutton.clicked.connect(self.accept)
        self.cancelbutton.clicked.connect(self.reject)
    def load(self):
        return [self.package_2.text(), self.destination.text(), self.cost.text()]


class LogsWindow(QDialog):
    def __init__(self):
        super(LogsWindow, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/logs.ui'
        uic.loadUi(main_ui_path, self)
        self.okbtn.clicked.connect(self.ok_btn)

    def ok_btn(self):
        self.hide()
