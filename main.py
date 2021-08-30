# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder:  File: main.py
#

import sys

from PyQt5.QtWidgets import QApplication

from speck_weg.ui.main_window import MainWindow
from speck_weg.db import CRUD


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":

    # tracebacks not printed if executed in ide
    sys.excepthook = except_hook

    # Open db session
    db = CRUD()

    # Start ui
    app = QApplication(sys.argv)
    win = MainWindow(db)
    win.show()
    sys.exit(app.exec())
