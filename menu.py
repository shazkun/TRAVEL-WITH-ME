from PyQt5.QtWidgets import *
from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QWidget
from prompts import *
import sys
import icons.resources_rc
from database import *
import authentication
from client import *
from packages import *
import authentication


class Main(QMainWindow, BaseWindow):
    def __init__(self, user_id):
        super(Main, self,).__init__()
        self.user_id = user_id

        main_ui_path = Path(__file__).resolve().parent / 'ui/main.ui'
        uic.loadUi(main_ui_path, self)
        self.table_widget = self.findChild(QTableWidget, 'tableWidget')
        self.profile_layout = self.profileframe.layout()

        self.button_clicked()
        self.db = DatabaseHandler()
        self.load_clients()
        self.table_flags()
        self.calendarDateChanged()
        self.setBackground()
        self.abg = authentication.AuthWindow()
        self.abg.setBackground(self.user_id)
        self.load_profiles()

    def table_flags(self):
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setColumnHidden(0, True)

    # LOAD CLIENTS

    def load_clients(self):
        self.tableWidget.setRowCount(0)  # Clear existing rows
        clients = self.db.fetch_user_clients(self.user_id)
        for client in clients:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for col, data in enumerate(client):
                self.tableWidget.setItem(
                    row_position, col, QTableWidgetItem(str(data)))

    def button_clicked(self):
        self.bgmode.clicked.connect(self.toggle_mode)
        # self.create_client.clicked.connect(self.add_client)
        self.packagesbtn.clicked.connect(self.view_packages)
        self.logsbtn.clicked.connect(self.view_logs)
        self.logoutbtn.clicked.connect(self.logout_btn)
        self.editbtn.clicked.connect(self.edit_client)
        self.addbtn.clicked.connect(self.add_client)
        self.delbtn.clicked.connect(self.delete_btn)
        self.calendarWidget.clicked.connect(self.calendarDateChanged)
        self.tabWidget.currentChanged.connect(self.calendarDateChanged)

    def load_profiles(self):
        users = ["User1", "User2", "User3", "User4", "User5", "User6", "User7", "User8", "User9", "User10",
                 "User11", "User12", "User13", "User14", "User15", "User16", "User17", "User18"]  # Example user names
        profileImagePath = 'icons/client.png'
        row = 0
        col = 0
        for user in users:
            userProfileWidget = UserProfileWidget(user, profileImagePath)
            self.profile_layout.addWidget(userProfileWidget, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

    def toggle_mode(self):
        # Get the current dark mode value from the database
        current_dark_mode = self.db.get_bg(self.user_id)

        # Toggle the dark mode value
        new_dark_mode = not current_dark_mode

        # Update the dark mode value in the database
        self.db.set_bg(self.user_id, new_dark_mode)

        # Update the UI based on the new dark mode value
        if not new_dark_mode:
            with open(Path(__file__).resolve().parent / "qss/light.css", "r") as file:
                # self.framebg.setStyleSheet(file.read())
                # self.tabWidget.setStyleSheet(file.read())
                self.setStyleSheet(file.read())
            pixmap = QPixmap('icons/BGL.png')
            self.label.setPixmap(pixmap)
            self.bgmode.setIcon(QIcon("icons/DRKMODE.png"))
        else:

            with open(Path(__file__).resolve().parent / "qss/dark.css", "r") as file:
                # self.framebg.setStyleSheet(file.read())
                # self.tabWidget.setStyleSheet(file.read())
                self.setStyleSheet(file.read())
            pixmap = QPixmap('icons/BGD.png')
            self.label.setPixmap(pixmap)
            self.bgmode.setIcon(QIcon("icons/LHTMODE.png"))

    def setBackground(self):
        getvalue = self.db.get_bg(self.user_id)
        if getvalue == True:
            with open("qss/dark.css", "r") as file:
                self.setStyleSheet(file.read())
            pixmap = QPixmap('icons/BGD.png')
            self.label.setPixmap(pixmap)
            self.bgmode.setIcon(QIcon("icons/LHTMODE.png"))

        if getvalue == False:
            with open("qss/light.css", "r") as file:
                self.setStyleSheet(file.read())
            pixmap = QPixmap('icons/BGL.png')
            self.label.setPixmap(pixmap)
            self.bgmode.setIcon(QIcon("icons/DRKMODE.png"))

    def calendarDateChanged(self):
        selected = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
    #     self.updateScheduleList(selected)

    # def updateScheduleList(self, date):
    #     self.listWidget.clear()  # Clear existing items
    #     clients = self.db.fetch_user_clients_by_date(self.user_id, date)
    #     for client in clients:
    #         c_id = client[0]
    #         destination = client[-1]  # Adjust index according to your data structure
    #         location = client[6]
    #         item_text = f"{c_id} Location: {location} Destination: {destination}"
    #         list_item = QListWidgetItem(item_text)
    #         self.listWidget.addItem(list_item)

    # ADD CLIENT FUNCTION

    def add_client(self):
        self.main = ScheduleWindow(self.tableWidget, self.db, self.user_id)
        self.main.setWindowModality(Qt.ApplicationModal)
        self.main.show()

    def view_packages(self):
        self.main = PackageWindow()
        self.main.setWindowModality(Qt.ApplicationModal)
        self.main.show()

    def view_logs(self):
        self.main = LogsWindow()
        self.main.setWindowModality(Qt.ApplicationModal)
        self.main.show()

    # UPDATE FUNCTION

    def edit_client(self):
        selected_items = self.tableWidget.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            # Assuming client_id is in the first column
            client_id_item = self.tableWidget.item(selected_row, 0)
            if client_id_item:
                client_id = int(client_id_item.text())
                current_details = {
                    'name': self.tableWidget.item(selected_row, 1).text(),
                    'contact': self.tableWidget.item(selected_row, 2).text(),
                    'date': self.tableWidget.item(selected_row, 3).text(),
                    'time': self.tableWidget.item(selected_row, 4).text(),
                    'pax': self.tableWidget.item(selected_row, 5).text(),
                    'location': self.tableWidget.item(selected_row, 6).text(),
                    'type': self.tableWidget.item(selected_row, 7).text(),
                    'destination': self.tableWidget.item(selected_row, 8).text()
                }
                edit_dialog = EditClientWindow(
                    self.db, self.user_id, client_id, None, self.table_widget)
                edit_dialog.name.setText(current_details['name'])
                edit_dialog.contact.setText(current_details['contact'])
                edit_dialog.date.setText(current_details['date'])
                edit_dialog.time.setText(current_details['time'])
                edit_dialog.pax.setText(current_details['pax'])
                edit_dialog.location.setText(current_details['location'])
                edit_dialog.typeCbox.setCurrentText(current_details['type'])
                edit_dialog.destination.setText(current_details['destination'])

                if edit_dialog.exec_() == QDialog.Accepted:
                    self.load_clients()  # Reload clients after editing
        else:
            QMessageBox.warning(self, 'No Selection',
                                'Please select a client to edit.')

    # DELETE SELECTED ROW

    def delete_selected_client(self, row):
        # Assuming the first column is the client ID
        client_id_item = self.tableWidget.item(row, 0)
        if client_id_item:
            client_id = client_id_item.text()
            self.db.delete_client(self.user_id, client_id)
            self.tableWidget.removeRow(row)

    def delete_btn(self):
        selected_items = self.tableWidget.selectedItems()
        dialog = ConfirmPrompt()
        dialog.setWindowTitle("Delete")
        pixmap = QPixmap('icons/warning.png')
        dialog.setCustomPixMap(pixmap, 1)
        if selected_items:

            if dialog.exec_() == QDialog.Accepted:
                selected_rows = sorted(set(item.row()
                                       for item in selected_items), reverse=True)
                for row in selected_rows:
                    print("Deleting row:", row)
                    self.delete_selected_client(row)
            else:
                pass
        else:
            QMessageBox.question(
                self,
                'No selected item!',
                'Please select an item first.',
                QMessageBox.Ok)

    def logout_btn(self):
        dialog = LogoutPrompt()
        self.auth = authentication.AuthWindow()
        if dialog.exec_() == QDialog.Accepted:
            self.hide()
            self.auth.show()
            self.auth.setBackground(self.user_id)
            if self.isMaximized():
                self.auth.showMaximized()
        else:
            pass


class UserProfileWidget(QFrame):
    def __init__(self, userName, profileImagePath):
        super().__init__()
        self.userName = userName
        self.profileImagePath = profileImagePath

        # Load the profile image and scale it to fit within 50x50 without cropping
        pixmap = QPixmap(profileImagePath)
        pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)

        # Create the profile label
        self.profileLabel = QLabel()
        self.profileLabel.setPixmap(pixmap)
        self.profileLabel.setAlignment(Qt.AlignCenter)

        # Set size policy to ensure the label can expand to fit the entire image
        self.profileLabel.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create the user name label
        self.userNameLabel = QLabel(userName)
        self.userNameLabel.setStyleSheet("font-size: 20px;")
        self.userNameLabel.setAlignment(Qt.AlignCenter)

        # Set up the layout for UserProfileWidget
        layout = QVBoxLayout(self)
        layout.addWidget(self.profileLabel)
        layout.addWidget(self.userNameLabel)
        self.userNameLabel.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
            background-color: #f0f0f0;
            border-radius: 5px;
            """)
        self.setStyleSheet("""
            UserProfileWidget:hover {
                background-color: #e0e0e0;
            }
        """)
