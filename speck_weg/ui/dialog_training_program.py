# fingertraining
# Stefan Hochuli, 20.07.2021,
# Folder: speck_weg/ui File: dialog_training_program.py
#


from typing import TYPE_CHECKING, Optional

from PyQt5.QtWidgets import QDialog
import PyQt5.QtCore

from ..models import TrainingProgramModel
from .dialog_training_program_ui import Ui_Dialog_training_program

if TYPE_CHECKING:
    from ..db import CRUD
    from ..models import TrainingThemeModel


user_role = PyQt5.QtCore.Qt.UserRole


class ProgramDialog(QDialog, Ui_Dialog_training_program):

    def __init__(self, db: 'CRUD', parent=None,
                 obj: 'TrainingProgramModel' = None, parent_tth: 'TrainingThemeModel' = None):
        super().__init__(parent)

        self.db = db

        self.tpr: Optional['TrainingProgramModel'] = obj
        self.parent_tth: 'TrainingThemeModel' = parent_tth

        self.setupUi(self)
        self.connect()

        if self.tpr:
            # editing
            self.lineEdit_name.setText(self.tpr.name)
            self.textEdit_description.setText(self.tpr.description)

    @property
    def max_sequence(self) -> int:
        if self.parent_tth.training_programs:
            return max([tpr.sequence for tpr in self.parent_tth.training_programs])
        else:
            return 0

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_save.clicked.connect(self.save)

    def save(self):
        # Return the object, add to the db from main window
        if self.tpr:
            print('editing')
            self.update_object()

            self.db.update()

            print('after update')
            for tex in self.tpr.training_exercises:
                print(tex, tex.sequence)
        else:
            print('new program')
            self.tpr = TrainingProgramModel(
                tpr_tth_id=self.parent_tth.tth_id,
                sequence=self.max_sequence + 1
            )

            self.update_object()
            self.db.create(self.tpr)
            print('tpr added to the database')

            # Clear after saving for adding a new one
            self.lineEdit_name.clear()
            self.textEdit_description.clear()
            # Reset the focus on the first lineEdit
            self.lineEdit_name.setFocus()
            self.tpr = None

    def refresh_exercise_list(self):
        for i, tpe in enumerate(self.tpr.training_exercises):
            self.listWidget_exercise.insertItem(i, tpe.training_exercise.name)
            self.listWidget_exercise.item(i).setData(user_role, tpe.training_exercise)

    def update_object(self):
        if self.tpr:
            self.tpr.name = self.lineEdit_name.text()
            self.tpr.description = self.textEdit_description.toPlainText()

        else:
            raise ValueError('No Training program object for updating.')
