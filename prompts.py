from PyQt5.QtWidgets import *
from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import Qt
import sys
import icons.resources_rc

class SavePrompt(QDialog):
    def __init__(self):
        super(SavePrompt, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/prompts/save.ui'
        uic.loadUi(main_ui_path, self)
        self.ok.clicked.connect(self.accept)
        self.cancel.clicked.connect(self.reject)
    
class ConfirmPrompt(QDialog):
    def __init__(self):
        super(ConfirmPrompt, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/prompts/confirm.ui'
        uic.loadUi(main_ui_path, self)
        self.ok.clicked.connect(self.accept)
        self.cancel.clicked.connect(self.reject)

    def setCustomPixMap(self, pixmap, label_index):
        if label_index == 1:
            self.label.setPixmap(pixmap)

class ExitPrompt(QDialog):
    def __init__(self):
        super(ExitPrompt, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/prompts/exit.ui'
        uic.loadUi(main_ui_path, self)
        self.ok.clicked.connect(self.accept)
        self.cancel.clicked.connect(self.reject)

class LogoutPrompt(QDialog):
    def __init__(self):
        super(LogoutPrompt, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/prompts/logout.ui'
        uic.loadUi(main_ui_path, self)
        self.ok.clicked.connect(self.accept)
        self.cancel.clicked.connect(self.reject)


class SuccessPrompt(QDialog):
    def __init__(self):
        super(SuccessPrompt, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/prompts/success.ui'
        uic.loadUi(main_ui_path, self)
        self.ok.clicked.connect(self.accept)

class DetailsProfile(QDialog):
    def __init__(self):
        super(DetailsProfile, self).__init__()
        main_ui_path = Path(__file__).resolve().parent / 'ui/viewclient.ui'
        uic.loadUi(main_ui_path, self)
        

class BaseWindow(QWidget):
    def __init__(self):
        super().__init__()
       

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            'Exit Confirmation',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

       

if __name__ == "__main__":
    from main import StartWindow
    app = QApplication(sys.argv)
    dialog = StartWindow()
    icon_path = Path(__file__).resolve().parent / "icons/logo.png"
    app_icon = QIcon(str(icon_path))
    app.setWindowIcon(app_icon)
    dialog.show()
    sys.exit(app.exec_())
