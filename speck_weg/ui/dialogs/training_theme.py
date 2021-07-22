# fingertraining
# Stefan Hochuli, 20.07.2021,
# Folder: speck_weg/ui/dialogs File: training_theme.py
#

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QDialog

from ...models import TrainingTheme
from .training_theme_ui import Ui_dialog_training_theme

if TYPE_CHECKING:
    from ...db import CRUD


class ThemeDialog(QDialog, Ui_dialog_training_theme):

    tth: 'TrainingTheme' = None

    def __init__(self, db: 'CRUD', parent=None, obj: 'TrainingTheme' = None):
        super().__init__(parent)
        print('init theme')

        self.db = db

        self.tth = obj

        self.setupUi(self)
        self.connect()

        if self.tth:
            self.set_edit_mode()
        else:
            self.set_new_mode()

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_save.clicked.connect(self.save)

    def save(self):
        # Return the object, add to the db from main window
        self.tth = TrainingTheme(
            name=self.lineEdit_name.text(),
            description=self.lineEdit_description.text()
        )
        self.db.create(self.tth)
        print('theme added to the database')

        # Clear after saving for adding a new one
        self.lineEdit_name.clear()
        self.lineEdit_description.clear()

    def set_edit_mode(self):
        self.pushButton_save.setEnabled(False)
        self.pushButton_apply.setEnabled(True)
        self.pushButton_apply.setDefault(True)

    def set_new_mode(self):
        self.pushButton_apply.setEnabled(False)
        self.pushButton_save.setEnabled(True)
        self.pushButton_save.setDefault(True)
