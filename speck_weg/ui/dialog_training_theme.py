# fingertraining
# Stefan Hochuli, 20.07.2021,
# Folder: speck_weg/ui File: dialog_training_theme.py
#

from typing import TYPE_CHECKING, Optional

from PyQt5.QtWidgets import QDialog

from ..models import TrainingThemeModel
from .dialog_training_theme_ui import Ui_Dialog_training_theme

if TYPE_CHECKING:
    from ..db import CRUD


class ThemeDialog(QDialog, Ui_Dialog_training_theme):

    def __init__(self, db: 'CRUD', parent=None, obj: 'TrainingThemeModel' = None,
                 max_sequence=None):
        super().__init__(parent)
        print('init theme')

        self.db = db

        self.tth: Optional['TrainingThemeModel'] = obj
        self.max_sequence: int = max_sequence

        self.setupUi(self)
        self.connect()

        if self.tth:
            # editing
            self.lineEdit_name.setText(self.tth.name)
            self.textEdit_description.setText(self.tth.description)

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_save.clicked.connect(self.save)

    def save(self):

        if self.tth:
            # editing the existing object
            self.tth.name = self.lineEdit_name.text()
            self.tth.description = self.textEdit_description.toPlainText()

            self.db.update()
            print('theme updated')

        else:
            # Return the object, add to the db from main window
            self.tth = TrainingThemeModel(
                name=self.lineEdit_name.text(),
                description=self.textEdit_description.toPlainText(),
                sequence=self.max_sequence + 1,
            )
            self.db.create(self.tth)
            self.max_sequence += 1
            print('theme added to the database')

            # Clear after saving for adding a new one
            self.tth = None
            self.lineEdit_name.clear()
            self.textEdit_description.clear()
            # Reset the focus on the first lineEdit
            self.lineEdit_name.setFocus()
