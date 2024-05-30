# # main.py

from database import DatabaseHandler

class Test:
    def __init__(self) -> None:
        self.data = DatabaseHandler('user_clients.db')

    def test(self):
        user1 = self.data.fetch_user_clients_one(1)
        if user1:
            print(f"Name of user with ID 1: {user1['name']}")
            # Access other columns using their names
        else:
            print("User not found or database is empty.")

ww = Test()
ww.test()

# from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Create a QListWidget and add items
#         self.listWidget = QListWidget()
#         self.listWidget.addItems(["Item 1", "Item 2", "Item 3"])

#         # Connect the itemSelectionChanged signal to a custom slot
#         self.listWidget.itemSelectionChanged.connect(self.on_item_selection_changed)

#         # Set layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.listWidget)

#         # Set the main widget and layout
#         main_widget = QWidget()
#         main_widget.setLayout(layout)
#         self.setCentralWidget(main_widget)

#         self.setWindowTitle("ListWidget Selected Item Event Example")

#     def on_item_selection_changed(self):
#         # Get the selected item in the list widget
#         selected_items = self.listWidget.selectedItems()
#         if selected_items:
#             # Get the text of the first selected item
#             text = selected_items[0].text()

#             # Extract numeric characters from the text
#             numbers = ''.join(filter(str.isdigit, text))
#             print("Numbers in the selected item text:", numbers)

# if __name__ == '__main__':
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec_()
