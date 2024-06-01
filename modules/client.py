from PyQt5.QtWidgets import *
from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QIcon, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp,QEvent
from PyQt5.QtWidgets import QWidget
from modules.prompts import *
import sys
import modules.icons.resources_rc
from modules.database import *
import re
import datetime

current_datetime = datetime.datetime.now()

# Format date and time separately
date_today = current_datetime.strftime("%Y-%m-%d")
time_today = current_datetime.strftime("%H:%M:%S")
class ClientWindow(QDialog, BaseWindow):
    def __init__(self, table, db, user_id, selected_date):
        super(ClientWindow, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/client.ui'
        uic.loadUi(main_ui_path, self)
        self.table = table
        self.sel_date = selected_date

        self.db= db
        self.user_id = user_id
        self.cancelbutton.clicked.connect(self.cancel_btn)
        self.savebutton.clicked.connect(self.save_btn)
        self.date.setText(self.sel_date)
        phone_validator = QRegExpValidator(QRegExp(r'^\d{10}$'))  # Regular expression for a 10-digit phone number
        self.contact.setValidator(phone_validator)
        self.typeCbox.currentIndexChanged.connect(self.selection_changed)
        self.selection_changed()

    def selection_changed(self):
        selected_items = self.typeCbox.currentText()
        if selected_items:
            match = re.search(r'ID:\s*(\d+)', selected_items)
            pid = match.group(1)
            cost = self.db.fetch_user_packages_one(self.user_id, pid)
            for i in cost:
                self.cost.setText(i['cost'])
                self.destination.setText(i['destination'])
        else: 
            pass
    def package_selector(self):
        package = self.db.fetch_user_packages(self.user_id)
        
        for item in package:
            name = f'ID: {item[0]} {item[1]}'
            self.typeCbox.addItem(name)



      
    def table_add(self):
        last_id = self.db.cursor.lastrowid
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(str(last_id)))
        self.table.setItem(row_position, 1, QTableWidgetItem(self.name.text()))
        self.table.setItem(row_position, 2, QTableWidgetItem(self.contact.text()))
        self.table.setItem(row_position, 3, QTableWidgetItem(self.date.text()))
        self.table.setItem(row_position, 4, QTableWidgetItem(self.time.text()))
        self.table.setItem(row_position, 5, QTableWidgetItem(self.pax.text()))
        self.table.setItem(row_position, 6, QTableWidgetItem(self.location.text()))
        type_cbox = self.typeCbox.currentText() 
        match = re.search(r'ID:\s*(?:\d+\s*)?([^\d\s]+)', type_cbox)
        type = match.group(1)
        self.table.setItem(row_position, 7, QTableWidgetItem(type))
        self.table.setItem(row_position, 8, QTableWidgetItem(self.destination.text()))
        self.table.setItem(row_position, 9, QTableWidgetItem(self.cost.text()))



    def cancel_btn(self):
        dialog = ExitPrompt()
        if dialog.exec_() == QDialog.Accepted:
            self.back_date = ScheduleWindow(self.table, self.db,self.user_id)
            self.back_date.show()
            self.hide()
        else:
            pass
    
    def save_btn(self):
        dialog = SavePrompt()
        if dialog.exec_() == QDialog.Accepted:
            name = self.name.text()
            contact = self.contact.text()
            date = self.sel_date
            time = self.time.text()
            pax = self.pax.text()
            location = self.location.text()
            type_cbox = self.typeCbox.currentText() 
            match = re.search(r'ID:\s*(?:\d+\s*)?([^\d\s]+)', type_cbox)
            type = match.group(1)
            destination = self.destination.text()
           
            cost = self.cost.text()
            # if not name or not contact or not date or not time or not pax or not location or not type or not destination or not cost:
            #     QMessageBox.warning(self, 'Add Client Failed', 'All fields are required')
            #     return
            self.db.insert_client(self.user_id, name, contact, date, time, pax, location, type, destination, cost)
            self.table_add()
            self.hide()
            self.db.insert_logs(self.user_id, date_today, time_today, 'add client')
        else:
            pass
        
class EditClientWindow(QDialog):
    def __init__(self, db, user_id, client_id, selected_date, table):
        super(EditClientWindow, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/client.ui'
        uic.loadUi(main_ui_path, self)
        self.setWindowTitle('Edit Client Details')
        self.db = db
        self.table = table
        self.user_id = user_id
        self.client_id = client_id
        self.sel_date = selected_date
        self.savebutton.clicked.connect(self.save_btn)
        self.cancelbutton.clicked.connect(self.cancel_btn)
        phone_validator = QRegExpValidator(QRegExp(r'^\d{10}$'))  # Regular expression for a 10-digit phone number
        self.contact.setValidator(phone_validator)
        self.date.installEventFilter(self)
        self.typeCbox.currentIndexChanged.connect(self.selection_changed)
        self.selection_changed()

    def selection_changed(self):
        selected_items = self.typeCbox.currentText()
        if selected_items:
            match = re.search(r'ID:\s*(\d+)', selected_items)
            pid = match.group(1)
            cost = self.db.fetch_user_packages_one(self.user_id, pid)
            for i in cost:
                self.cost.setText(i['cost'])
                self.destination.setText(i['destination'])
        else: 
            pass
    def package_selector(self):
        package = self.db.fetch_user_packages(self.user_id)
        
        for item in package:
            name = f'ID: {item[0]} {item[1]}'
            self.typeCbox.addItem(name)
        
    
    def eventFilter(self, source, event):
        if source is self.date and event.type() == QEvent.MouseButtonPress:
            self.open_calendar_dialog()
            return True
        return super().eventFilter(source, event)



    def open_calendar_dialog(self):
        # Open the CalendarEdit dialog
        dialog = CalendarEdit()
        if dialog.exec_() == QDialog.Accepted:
            self.selected_date = dialog.calendarWidget.selectedDate()
            print("Selected date:", self.selected_date.toString(Qt.ISODate))
            self.update_date_label()
        else:
            print("Dialog canceled")

    def update_date_label(self):
        # Update the date label with the selected date
        if self.selected_date is not None:
            self.date.setText(self.selected_date.toString(Qt.ISODate))
            

    def save_btn(self):
        dialog = SavePrompt()
        name = self.name.text()
        contact = self.contact.text()
        date = self.date.text()
        time = self.time.text()
        pax = self.pax.text()
        location = self.location.text()
        type = self.typeCbox.currentText()
        destination = self.destination.text()
        cost = self.cost.text()
        if dialog.exec_() == QDialog.Accepted:
            # if not name or not contact or not date or not time or not pax or not location or not type or not destination:
            #     QMessageBox.warning(self, 'Update Client Failed', 'All fields are required')
            #     return
            self.db.update_client(self.user_id, self.client_id, name, contact, date, time, pax, location, type, destination, cost)
            self.accept()  # Close the dialog 
            self.lclients()
            self.db.insert_logs(self.user_id, date_today, time_today, 'update client')
        else:
            pass
    def lclients(self):
        self.table.setRowCount(0)  # Clear existing rows
        clients = self.db.fetch_user_clients(self.user_id)
        for client in clients:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col, data in enumerate(client):  
                self.table.setItem(row_position, col, QTableWidgetItem(str(data)))


    def cancel_btn(self):
        dialog = ExitPrompt()
        if dialog.exec_() == QDialog.Accepted:
            self.hide()
        else:
            self.main = ScheduleWindow(self.tableWidget, self.db, self.user_id)
            self.main.setWindowModality(Qt.ApplicationModal)
            self.main.show()
            

        

        
class ScheduleWindow(QDialog, BaseWindow):
    def __init__(self, table, db, user_id):
        super(ScheduleWindow, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/schedule.ui'
        uic.loadUi(main_ui_path, self)
        self.table = table
        self.db = db
        self.user_id = user_id
        self.calendarWidget.clicked.connect(self.calendarDateChanged)
        self.okbtn.clicked.connect(self.add_client)
        self.okbtn.clicked.connect(self.update)
        self.calendarDateChanged()
        
        self.updatebtn.clicked.connect(self.update_client_button)


    def calendarDateChanged(self):
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        self.list_clients(selected_date)
        

    def add_client(self):
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        self.menu = ClientWindow(self.table, self.db, self.user_id, selected_date)
        self.menu.selection_changed()
        self.menu.show()
        self.db.insert_logs(self.user_id, date_today, time_today, 'add client')
        self.hide()
    

    def update_client_button(self):
        selected_items = self.listWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'No Selection', 'Please select an item to update.')
            return
        text = selected_items[0].text()
        match = re.search(r'ID:\s*(\d+)', text)
        client_id = match.group(1)
        
        print(client_id)
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        current_details = self.db.fetch_user_clients_one(self.user_id, client_id)  
        if current_details:
            self.update_client(client_id, current_details, selected_date)
            self.db.insert_logs(self.user_id, date_today, time_today, 'update client')
        else:
            QMessageBox.warning(self, 'Client Not Found', 'Client details not found for the selected client ID.')

    def update_client(self, client_id, current_details, selected_date):
        self.menu = EditClientWindow(self.db, self.user_id, client_id, selected_date, self.table)
        if current_details:
            self.menu.name.setText(current_details.get('name', ''))
            self.menu.contact.setText(current_details.get('contact', ''))
            self.menu.date.setText(current_details.get('date', ''))
            self.menu.time.setText(current_details.get('time', ''))
            self.menu.pax.setText(current_details.get('pax', ''))
            self.menu.location.setText(current_details.get('location', ''))
            self.menu.typeCbox.setCurrentText(current_details.get('type', ''))
            self.menu.destination.setText(current_details.get('destination', ''))
            self.menu.destination.setText(current_details.get('cost', ''))
            self.menu.show()
            self.hide()


    
    def list_clients(self, selected_date):
        self.listWidget.clear()  # Clear existing items
        clients = self.db.fetch_user_clients_by_date(self.user_id, selected_date)
        for client in clients:
            c_id = client[0]
            location = client[6]
            destination = client[-1]  # Adjust index according to your data structure
            
            item_text = f"ID: {c_id} Location: {location} Destination: {destination}"
            list_item = QListWidgetItem(item_text)
            self.listWidget.addItem(list_item)

