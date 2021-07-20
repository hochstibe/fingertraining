# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder:  File: main.py
#

import sys

from PyQt5.QtWidgets import QApplication

from speck_weg.ui.main_window import Window


if __name__ == "__main__":

    # Start ui
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
