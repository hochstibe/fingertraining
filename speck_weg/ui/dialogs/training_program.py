# fingertraining
# Stefan Hochuli, 20.07.2021, 
# Folder: speck_weg/ui/dialogs File: training_program.py
#

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QDialog

from ...models import TrainingProgram
from .training_program_ui import Ui_dialog_training_program

if TYPE_CHECKING:
    from ...db import CRUD


class ProgramDialog(QDialog, Ui_dialog_training_program):

    tpr: 'TrainingProgram' = None

    def __init__(self, db: 'CRUD', parent=None, obj: 'TrainingProgram' = None):
        super().__init__(parent)

        self.db = db

        self.tpr = obj

        self.setupUi(self)
        self.connect()

        if self.tpr:
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
        self.tpr = TrainingProgram(
            name=self.lineEdit_name.text(),
            description=self.lineEdit_description.text()
        )
        self.db.create(self.tpr)
        print('tpr added to the database')

    def set_edit_mode(self):
        self.pushButton_save.setEnabled(False)
        self.pushButton_apply.setEnabled(True)
        self.pushButton_apply.setDefault(True)

    def set_new_mode(self):
        self.pushButton_apply.setEnabled(False)
        self.pushButton_save.setEnabled(True)
        self.pushButton_save.setDefault(True)
