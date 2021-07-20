# fingertraining
# Stefan Hochuli, 20.07.2021, 
# Folder: speck_weg/ui/dialogs File: training_program.py
#

from PyQt5.QtWidgets import QDialog

from ...db import session
from ...models import TrainingProgram
from .training_program_ui import Ui_dialog_training_program


class ProgramDialog(QDialog, Ui_dialog_training_program):

    tpr: 'TrainingProgram' = None

    def __init__(self, parent=None, obj: 'TrainingProgram' = None):
        super().__init__(parent)

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
            tpr_name=self.lineEdit_tpr_name.text(),
            tpr_description=self.lineEdit_tpr_description.text()
        )
        session.add(self.tpr)
        session.commit()
        print('tpr added to the database')

    def set_edit_mode(self):
        self.pushButton_save.setEnabled(False)
        self.pushButton_apply.setEnabled(True)

    def set_new_mode(self):
        self.pushButton_save.setEnabled(True)
        self.pushButton_apply.setEnabled(False)