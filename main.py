from PyQt5.QtWidgets import *
from PyQt5 import uic
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QWidget
import start
import sys


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = start.StartWindow()
    icon_path = Path(__file__).resolve().parent / "icons/logo.png"
    app_icon = QIcon(str(icon_path))
    app.setWindowIcon(app_icon)
    dialog.show()
    sys.exit(app.exec_())
