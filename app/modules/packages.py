from PyQt5.QtWidgets import *
from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIntValidator,QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
from modules.prompts import *
import modules.icons.resources_rc
from modules.database import *
import modules.authentication
from modules.client import ClientWindow
import datetime

current_datetime = datetime.datetime.now()

# Format date and time separately
date_today = current_datetime.strftime("%Y-%m-%d")
time_today = current_datetime.strftime("%H:%M:%S")





class PackageWindow(QDialog):
    def __init__(self, user_id):
        super(PackageWindow, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/package.ui'
        uic.loadUi(main_ui_path, self)
        self.db = DatabaseHandler()
        self.user_id = user_id
        self.table_widget = self.findChild(QTableWidget, 'tableWidget')
        self.okbtn.clicked.connect(self.ok_btn)
        self.addbtn.clicked.connect(self.add_package)
        self.editbtn.clicked.connect(self.update_package)
        self.delbtn.clicked.connect(self.delete_package)
        self.table_flags()
        

        self.load_packages()
        self.main = PackageAddPrompt(self.user_id, self.table_widget)
        client_validator = QIntValidator(0,2147483647)  # Set the range from 0 to 9999999999
        self.main.cost.setValidator(client_validator)

    def table_flags(self):
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setColumnHidden(0, True)

    def ok_btn(self):
        self.hide()
    
    def add_package(self):
        self.main.show()
        self.main.package_2.clear()
        self.main.destination.clear()
        self.main.cost.clear()
        self.main.setWindowModality(Qt.ApplicationModal)

    def load_packages(self):
        self.table_widget.setRowCount(0)  # Clear existing rows
        clients = self.db.fetch_user_packages(self.user_id)
        for client in clients:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            for col, data in enumerate(client):
                self.table_widget.setItem(row_position, col, QTableWidgetItem(str(data)))

    
    def update_package(self):
        selected_items = self.table_widget.selectedItems() 
        if selected_items:
            selected_row = selected_items[0].row()
            # Assuming client_id is in the first column
            package_id_item = self.tableWidget.item(selected_row, 0)
            if package_id_item:
                package_id = int(package_id_item.text())
                current_details = {
                    'package_type': self.table_widget.item(selected_row, 1).text(),
                    'destination': self.table_widget.item(selected_row, 2).text(),
                    'cost': self.table_widget.item(selected_row, 3).text()
                }
                self.main = EditPackage(self.user_id, self.table_widget)
                self.main.package_2.setText(current_details['package_type'])
                self.main.destination.setText(current_details['destination'])
                self.main.cost.setText(current_details['cost'])
               
                # self.db.update_package(self.user_id,package_id, package_type, destination, cost)
                self.main.show()
                self.load_packages()  # Reload clients after editing
                
            
        else:
            QMessageBox.warning(self, 'No Selection',
                                'Please select a client to edit.')


    def delete_package(self):
        selected_items = self.table_widget.selectedItems()
       
        selected_row = self.table_widget.currentRow()
        current_details = {
                    'type': self.tableWidget.item(selected_row, 1).text(),
                    'destination': self.tableWidget.item(selected_row, 2).text(),
                    'cost': self.tableWidget.item(selected_row, 3).text()
                }

        dialog = ConfirmPrompt()
        dialog.setWindowTitle("Delete")
        pixmap = QPixmap(str(Path(__file__).resolve().parent / 'icons/warning.png'))
        dialog.setCustomPixMap(pixmap, 1)
        if selected_items:
            if dialog.exec_() == QDialog.Accepted:
                package_id = self.table_widget.item(selected_row, 0).text()
                self.db.delete_package(package_id, self.user_id, current_details['type'],current_details['cost'],current_details['destination'])
                self.load_packages()
                 
            else:
                pass
        else:
            QMessageBox.question(
                self,
                'No selected item!',
                'Please select an item first.',
                QMessageBox.Ok)

class EditPackage(QDialog):
    def __init__(self, user_id, table):
        super(EditPackage, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/p_forms.ui'
        uic.loadUi(main_ui_path, self)
        self.savebutton.clicked.connect(self.update_p)
        self.cancelbutton.clicked.connect(self.hide)
        self.db = DatabaseHandler()
        self.user_id = user_id
        self.table= table
        regex = QRegExp("[a-zA-Z ]+")
        validator = QRegExpValidator(regex)
        self.package_2.setValidator(validator)
    def update_p(self):
       
        selected_row = self.table.currentRow()
        current_details = {
                    'type': self.table.item(selected_row, 1),
                    'destination': self.table.item(selected_row, 2),
                    'cost': self.table.item(selected_row, 3)
                }

        dialog = SavePrompt()
        if dialog.exec_() == QDialog.Accepted:
            pid = self.table.item(selected_row,0)
            self.db.update_package(self.user_id,pid,current_details['type'],current_details['destination'],current_details['cost'])
            self.load_packages()
            self.accept()

    def load_packages(self):
        self.table.setRowCount(0)  # Clear existing rows
        clients = self.db.fetch_user_packages(self.user_id)
        for client in clients:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col, data in enumerate(client):
                self.table.setItem(row_position, col, QTableWidgetItem(str(data)))
class PackageAddPrompt(QDialog):
    def __init__(self, user_id, table):
        super(PackageAddPrompt, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/p_forms.ui'
        uic.loadUi(main_ui_path, self)
        self.savebutton.clicked.connect(self.add_package)
        self.cancelbutton.clicked.connect(self.hide)
        self.db = DatabaseHandler()
        self.user_id = user_id
        self.table= table
        regex = QRegExp("[a-zA-Z ]+")
        validator = QRegExpValidator(regex)
        self.package_2.setValidator(validator)
    def load_packages(self):
        self.table.setRowCount(0)  # Clear existing rows
        clients = self.db.fetch_user_packages(self.user_id)
        for client in clients:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col, data in enumerate(client):
                self.table.setItem(row_position, col, QTableWidgetItem(str(data)))
    # def add_package(self):
    #     package = self.package_2.text()
    #     destination = self.destination.text()
    #     cost = self.cost.text()
    #     dialog = SavePrompt()
    #     if dialog.exec_() == QDialog.Accepted:
    #         if self.cost.text() == '' or self.package_2.text() == '' or self.destination.text() == '':
    #             QMessageBox.warning(self, 'Add package Failed', 'All fields are required')
    #         else:
    #             self.db.insert_package(self.user_id, package, destination, cost)
    #             self.load_packages()
    #             self.accept() 
    def add_package(self):
        package = self.package_2.text()
        destination = self.destination.text()
        cost = self.cost.text()
        dialog = SavePrompt()

        if dialog.exec_() == QDialog.Accepted:
            if not package or not destination or not cost:
                QMessageBox.warning(self, 'Add Package Failed', 'All fields are required')
                return

            # Check if package with the same type or cost already exists
            if self.db.package_exists(self.user_id, package, cost):
                QMessageBox.warning(self, 'Add Package Failed', 'Package with the same type or cost already exists')
                return

            self.db.insert_package(self.user_id, package, destination, cost)
            self.load_packages()
            self.accept()

    
    def cancelbtn(self):
        self.hide()

   


class LogsWindow(QDialog):
    def __init__(self, user_id):
        super(LogsWindow, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/logs.ui'
        uic.loadUi(main_ui_path, self)
        self.user_id = user_id 
        self.db = DatabaseHandler()
        self.table_widget = self.findChild(QTableWidget, 'tableWidget')
        self.load_logs()
        self.table_flags()
        self.okbtn.clicked.connect(self.ok_btn)
        self.delbtn.clicked.connect(self.delete_logs)
        
    def table_flags(self):
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setColumnHidden(0, True)

    def delete_logs(self):
        selected_items = self.table_widget.selectedItems()
        selected_row = self.table_widget.currentRow()
        dialog = ConfirmPrompt()
        dialog.setWindowTitle("Delete")
        pixmap = QPixmap(str(Path(__file__).resolve().parent/'icons/warning.png'))
        dialog.setCustomPixMap(pixmap, 1)
        if selected_items:
            if dialog.exec_() == QDialog.Accepted:
                package_id = self.table_widget.item(selected_row, 0).text()
                self.db.delete_logs(package_id)
                self.load_logs()
            else:
                pass
        else:
            QMessageBox.question(
                self,
                'No selected item!',
                'Please select an item first.',
                QMessageBox.Ok)
    def load_logs(self):
        self.table_widget.setRowCount(0)  # Clear existing rows
        clients = self.db.fetch_data(self.user_id)
        for client in clients:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            for col, data in enumerate(client):
                self.table_widget.setItem(row_position, col, QTableWidgetItem(str(data)))

    def ok_btn(self):
        self.hide()
