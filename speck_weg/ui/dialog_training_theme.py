# fingertraining
# Stefan Hochuli, 20.07.2021,
# Folder: speck_weg/ui File: dialog_training_theme.py
#

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QDialog

from .dialog_training_theme_ui import Ui_Dialog_training_theme
from ..app import TrainingTheme

if TYPE_CHECKING:
    from ..db import CRUD


class ThemeDialog(TrainingTheme, QDialog, Ui_Dialog_training_theme):

    def __init__(self, db: 'CRUD', tth_id: int = None, max_sequence=None,
                 parent=None):
        super().__init__(db=db, tth_id=tth_id, max_sequence=max_sequence, parent=parent)
        print('init theme')

        self.setupUi(self)
        self.connect()

        self.update_widgets()

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_save.clicked.connect(self.save)

    def save(self):

        if self.model:
            # editing the existing object
            self.edit_theme(self.lineEdit_name.text(), self.textEdit_description.toPlainText())
            print('theme updated')

        else:
            # Return the object, add to the db from main window
            self.add_theme(self.lineEdit_name.text(), self.textEdit_description.toPlainText())
            print('theme added to the database')

            self.update_widgets()

    def update_widgets(self):
        # updates the widgets from the model
        if self.model:
            # editing -> get values from model
            self.lineEdit_name.setText(self.model.name)
            self.textEdit_description.setText(self.model.description)
        else:
            # No model -> clear fields
            self.lineEdit_name.clear()
            self.textEdit_description.clear()
            # Reset the focus on the first lineEdit
            self.lineEdit_name.setFocus()
