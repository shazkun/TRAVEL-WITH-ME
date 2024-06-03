from PyQt5.QtWidgets import *
from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from modules.prompts import *
import sys
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
    def __init__(self, db, user_id):
        super(PackageWindow, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/package.ui'
        uic.loadUi(main_ui_path, self)
        self.db = db
        self.user_id = user_id
        self.table_widget = self.findChild(QTableWidget, 'tableWidget')
        self.okbtn.clicked.connect(self.ok_btn)
        self.addbtn.clicked.connect(self.add_package)
        self.editbtn.clicked.connect(self.update_package)
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
                self.table_widget.setItem(row_position, col, QTableWidgetItem(str(data)))

    def add_package(self):
        self.main = PackageAddPrompt()
        if self.main.exec_() == QDialog.Accepted:
            i = self.main.load()
            self.db.insert_package(self.user_id, i[0], i[1], i[2])
            self.load_packages()


    # def update_package(self):
    #     self.main = PackageAddPrompt()
    #     selected_items = self.table_widget.selectedItems()
    #     if not selected_items:
    #         QMessageBox.warning(self, 'No Selection', 'Please select an item to update.')
    #         return

    #     selected_row = self.table_widget.currentRow()
    #     package_id = int(self.table_widget.item(selected_row, 0).text())  # Assuming the first column is the package ID
    #     package_type = self.main.package_2.text()
    #     destination = self.main.destination.text()
    #     cost = self.main.cost.text()
    #     i = self.db.fetch_user_packages_one(self.user_id, package_id)  
    #     self.main.package_2.setText(i.get('package_type', ''))
    #     self.main.destination.setText(i.get('destination', ''))
    #     self.main.cost.setText(i.get('cost', ''))
    #     if self.main.exec_() == QDialog.Accepted:
    #         self.db.update_package(package_id, package_type, destination, cost)
    #         self.load_packages()
    
    def update_package(self):
        selected_items = self.tableWidget.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            # Assuming client_id is in the first column
            package_id_item = self.tableWidget.item(selected_row, 0)
            if package_id_item:
                package_id = int(package_id_item.text())
                current_details = {
                    'package_type': self.tableWidget.item(selected_row, 1).text(),
                    'destination': self.tableWidget.item(selected_row, 2).text(),
                    'cost': self.tableWidget.item(selected_row, 3).text()
                }
                edit_dialog = PackageAddPrompt()
                edit_dialog.package_2.setText(current_details['package_type'])
                edit_dialog.destination.setText(current_details['destination'])
                edit_dialog.cost.setText(current_details['cost'])

                if edit_dialog.exec_() == QDialog.Accepted:
                    package_type = edit_dialog.package_2.text()
                    destination = edit_dialog.destination.text()
                    cost = edit_dialog.cost.text()
                    self.db.update_package(package_id, package_type, destination, cost)
                    self.load_packages()  # Reload clients after editing
            
        else:
            QMessageBox.warning(self, 'No Selection',
                                'Please select a client to edit.')


    def delete_package(self):
        selected_items = self.table_widget.selectedItems()
       
        selected_row = self.table_widget.currentRow()

        dialog = ConfirmPrompt()
        dialog.setWindowTitle("Delete")
        pixmap = QPixmap('icons/warning.png')
        dialog.setCustomPixMap(pixmap, 1)
        if selected_items:
            if dialog.exec_() == QDialog.Accepted:
                package_id = self.table_widget.item(selected_row, 0).text()
                self.db.delete_package(package_id, self.user_id)
                self.db.insert_logs(self.user_id, date_today, time_today, 'delete package')
                self.load_packages()
        
            else:
                pass
        else:
            QMessageBox.question(
                self,
                'No selected item!',
                'Please select an item first.',
                QMessageBox.Ok)
        


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
    def __init__(self, user_id, db):
        super(LogsWindow, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/logs.ui'
        uic.loadUi(main_ui_path, self)
        self.user_id = user_id 
        self.db = db
        self.table_widget = self.findChild(QTableWidget, 'tableWidget')
        self.load_logs()
        self.table_flags()
        



        self.okbtn.clicked.connect(self.ok_btn)
        self.delbtn.clicked.connect(self.delete_logs)

        
    def table_flags(self):
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)


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
                self.db.delete_package(package_id)
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
