from PyQt5.QtWidgets import *
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from modules.start import *
import sys



        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = StartWindow()
    icon_path = Path(__file__).resolve().parent / "modules/icons/logo.png"
    app_icon = QIcon(str(icon_path))
    app.setWindowIcon(app_icon)
    dialog.show()
    sys.exit(app.exec_())
