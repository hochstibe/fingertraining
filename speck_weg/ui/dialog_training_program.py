# fingertraining
# Stefan Hochuli, 20.07.2021,
# Folder: speck_weg/ui File: dialog_training_program.py
#

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QDialog
import PyQt5.QtCore

from .dialog_training_program_ui import Ui_Dialog_training_program
from ..app import TrainingProgram

if TYPE_CHECKING:
    from ..db import CRUD


user_role = PyQt5.QtCore.Qt.UserRole


class ProgramDialog(TrainingProgram, QDialog, Ui_Dialog_training_program):

    def __init__(self, db: 'CRUD', tpr_tth_id: int, tpr_id: int = None, max_sequence: int = None,
                 parent=None):
        super().__init__(db=db, tpr_tth_id=tpr_tth_id, tpr_id=tpr_id, max_sequence=max_sequence,
                         parent=parent)

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
        # Return the object, add to the db from main window
        if self.model:
            print('editing')
            self.edit_program(self.lineEdit_name.text(), self.textEdit_description.toPlainText())

        else:
            print('new program')
            self.add_program(self.lineEdit_name.text(), self.textEdit_description.toPlainText())
            print('tpr added to the database')

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
