# fingertraining
# Stefan Hochuli, 22.07.2021,
# Folder: speck_weg/ui/dialogs File: workout.py
#


from typing import Dict, Optional, TYPE_CHECKING

from PyQt5.QtWidgets import QDialog

from ...models import WorkoutSession, WorkoutExercise, TrainingExercise
from .workout_ui import Ui_Dialog_workout

if TYPE_CHECKING:
    from ...db import CRUD
    from ...models import TrainingProgram


class WorkoutDialog(QDialog, Ui_Dialog_workout):

    session: 'WorkoutSession' = None

    exercises: Dict['TrainingExercise', Optional[WorkoutExercise]] = []

    def __init__(self, db: 'CRUD', parent=None,
                 obj: 'WorkoutSession' = None, parent_tpr: 'TrainingProgram' = None):
        super().__init__(parent)

        self.db = db

        self.session = obj
        self.parent_tpr = parent_tpr

        self.setupUi(self)
        self.connect()

        if self.session:
            self.set_edit_mode()
        else:
            self.set_new_mode()

            self.session = WorkoutSession()
            # Commit the workout session with the first exercise
            self.db.session.add(self.session)

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_save_exercise.clicked.connect(self.save_exercise)
        self.pushButton_previous.clicked.connect(self.previous_exercise)
        self.pushButton_next.clicked.connect(self.next_exercise)

    def save_exercise(self):
        # Return the object, add to the db from main window
        wex = WorkoutExercise(
            wex_wse_id=self.wse.wse_id,
            wex_tex_id=self.parent_tpr.tpr_id,
            repetitions=self.lineEdit_repetitions.text(),
            weight=self.lineEdit_weight.text()
        )
        self.db.session.add(wex)
        self.db.session.commit()
        print('tex added to the database')

        # Clear after saving for adding a new one
        self.lineEdit_name.clear()
        self.lineEdit_description.clear()

    def set_edit_mode(self):
        # self.pushButton_save.setEnabled(False)
        # self.pushButton_apply.setEnabled(True)
        # self.pushButton_apply.setDefault(True)
        pass

    def set_new_mode(self):
        # self.pushButton_apply.setEnabled(False)
        # self.pushButton_save.setEnabled(True)
        # self.pushButton_save.setDefault(True)
        pass
