# fingertraining
# Stefan Hochuli, 20.07.2021, 
# Folder: speck_weg/ui/dialogs File: training_exercise.py
#


from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QDialog

from ...models import TrainingExercise
from .training_exercise_ui import Ui_dialog_training_exercise

if TYPE_CHECKING:
    from ...db import CRUD
    from ...models import TrainingPlan


class ExerciseDialog(QDialog, Ui_dialog_training_exercise):

    tex: 'TrainingExercise' = None

    def __init__(self, db: 'CRUD', parent=None, obj: 'TrainingExercise' = None, parent_tpl: 'TrainingPlan' = None):
        super().__init__(parent)

        self.db = db

        self.tex = obj
        self.parent_tpl = parent_tpl

        self.setupUi(self)
        self.connect()

        if self.tex:
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
        self.tex = TrainingExercise(
            tex_tpl_id=self.parent_tpl.tpl_id,
            name=self.lineEdit_name.text(),
            description=self.lineEdit_description.text()
        )
        self.db.create(self.tex)
        print('tex added to the database')

    def set_edit_mode(self):
        self.pushButton_save.setEnabled(False)
        self.pushButton_apply.setEnabled(True)
        self.pushButton_apply.setDefault(True)

    def set_new_mode(self):
        self.pushButton_apply.setEnabled(False)
        self.pushButton_save.setEnabled(True)
        self.pushButton_save.setDefault(True)
