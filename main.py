# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder:  File: main.py
#

import sys

from PyQt5.QtWidgets import QApplication

from speck_weg.ui.main_window import Window
from speck_weg.db import CRUD


if __name__ == "__main__":

    # Open db session
    db = CRUD()

    # Start ui
    app = QApplication(sys.argv)
    win = Window(db)
    win.show()
    sys.exit(app.exec())
