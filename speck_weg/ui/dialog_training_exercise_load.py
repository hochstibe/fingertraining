# fingertraining
# Stefan Hochuli, 27.08.2021,
# Folder: speck_weg/ui File: dialog_training_exercise_load.py
#

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QDialog
import PyQt5.QtCore

from sqlalchemy import select

from ..models import TrainingExerciseModel, TrainingProgramExerciseModel
from .dialog_training_exercise_load_ui import Ui_Dialog_training_exercise_load

if TYPE_CHECKING:
    from ..db import CRUD
    from ..models import TrainingProgramModel, UserModel


user_role = PyQt5.QtCore.Qt.UserRole


class ExerciseLoadDialog(QDialog, Ui_Dialog_training_exercise_load):

    # tex: Optional['TrainingExercise'] = None
    # max_sequence: int = 0  # ordering sequence for the exercises, starting from 1

    def __init__(self, db: 'CRUD', parent=None, parent_tpr: 'TrainingProgramModel' = None,
                 usr: 'UserModel' = None):
        super().__init__(parent)

        self.db = db

        self.parent_tpr: 'TrainingProgramModel' = parent_tpr
        self.usr: 'UserModel' = usr

        self.setupUi(self)
        self.connect()

        self.checkBox_weight.setEnabled(False)
        self.checkBox_body_weight.setEnabled(False)
        self.checkBox_duration.setEnabled(False)

        self.fill_exercise_list()

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_import.clicked.connect(self.import_exercise)
        self.listWidget_exercise.clicked.connect(self.exercise_list_clicked)

    def fill_exercise_list(self):

        stmt = select(TrainingExerciseModel).order_by(TrainingExerciseModel.name)

        exercises = self.db.read_stmt(stmt)

        for i, tex in enumerate(exercises):
            self.listWidget_exercise.insertItem(i, tex.name)
            self.listWidget_exercise.item(i).setData(user_role, tex)

    def exercise_list_clicked(self):
        exercise = self.listWidget_exercise.currentItem()
        print('Clicked on the exercise list', exercise.text())

        tex: 'TrainingExerciseModel' = exercise.data(user_role)

        self.lineEdit_name.setText(tex.name)
        self.textEdit_description.setText(tex.description)
        self.spinBox_sets.setValue(tex.baseline_sets)
        self.spinBox_repetitions.setValue(tex.baseline_repetitions)

        self.checkBox_weight.setChecked(False)
        self.checkBox_body_weight.setChecked(False)
        if tex.baseline_weight:
            self.checkBox_weight.setChecked(True)
            self.doubleSpinBox_weight.setValue(tex.baseline_weight)
        if tex.tex_usr_id:
            self.checkBox_weight.setChecked(True)
            self.checkBox_body_weight.setChecked(True)
            self.doubleSpinBox_weight.setValue(self.usr.weight)
        if tex.baseline_duration:
            self.checkBox_duration.setChecked(True)
            self.doubleSpinBox_duration.setValue(tex.baseline_duration)

    def import_exercise(self):

        exercise = self.listWidget_exercise.currentItem()

        if exercise:
            # Add the a new relation
            try:
                if self.parent_tpr.training_exercises:
                    max_sequence = max([tpr.sequence for tpr in self.parent_tpr.training_exercises])
                else:
                    max_sequence = 0
                tpe = TrainingProgramExerciseModel(sequence=max_sequence + 1)
                tpe.training_exercise = exercise.data(user_role)
                tpe.training_program = self.parent_tpr
                # self.parent_tpr.training_exercises.append(exercise.data(user_role))
                self.db.update()
            except Exception as exc:
                print(exc)
                raise
