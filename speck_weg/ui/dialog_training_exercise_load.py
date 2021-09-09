# fingertraining
# Stefan Hochuli, 27.08.2021,
# Folder: speck_weg/ui File: dialog_training_exercise_load.py
#

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QDialog
import PyQt5.QtCore

from ..app import TrainingExerciseCollection
from .dialog_training_exercise_load_ui import Ui_Dialog_training_exercise_load

if TYPE_CHECKING:
    from ..db import CRUD


user_role = PyQt5.QtCore.Qt.UserRole


class ExerciseLoadDialog(TrainingExerciseCollection, QDialog, Ui_Dialog_training_exercise_load):

    # tex: Optional['TrainingExercise'] = None
    # max_sequence: int = 0  # ordering sequence for the exercises, starting from 1

    def __init__(self, db: 'CRUD', tpr_id: int, usr_id: int,
                 parent=None):
        super().__init__(db=db, tpr_id=tpr_id, usr_id=usr_id, parent=parent)

        self.db = db

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
        self.pushButton_import.clicked.connect(self.import_exercise_clicked)
        self.listWidget_exercise.clicked.connect(self.exercise_list_clicked)

    def fill_exercise_list(self):

        for i, tex in enumerate(self.model_list):
            self.listWidget_exercise.insertItem(i, tex.name)
            self.listWidget_exercise.item(i).setData(user_role, tex.tex_id)

    def exercise_list_clicked(self):
        exercise = self.listWidget_exercise.currentItem()
        print('Clicked on the exercise list', exercise.text())

        self.current_tex_id = exercise.data(user_role)

        self.lineEdit_name.setText(self.current_model.name)
        self.textEdit_description.setText(self.current_model.description)
        self.spinBox_sets.setValue(self.current_model.baseline_sets)
        self.spinBox_repetitions.setValue(self.current_model.baseline_repetitions)

        self.checkBox_weight.setChecked(False)
        self.checkBox_body_weight.setChecked(False)
        if self.current_model.baseline_weight:
            self.checkBox_weight.setChecked(True)
            self.doubleSpinBox_weight.setValue(self.current_model.baseline_weight)
        if self.current_model.tex_usr_id:
            self.checkBox_weight.setChecked(True)
            self.checkBox_body_weight.setChecked(True)
            self.doubleSpinBox_weight.setValue(self.user_model.weight)
        if self.current_model.baseline_duration:
            self.checkBox_duration.setChecked(True)
            self.doubleSpinBox_duration.setValue(self.current_model.baseline_duration)

        # tex: 'TrainingExerciseModel' = exercise.data(user_role)
        #
        # self.lineEdit_name.setText(tex.name)
        # self.textEdit_description.setText(tex.description)
        # self.spinBox_sets.setValue(tex.baseline_sets)
        # self.spinBox_repetitions.setValue(tex.baseline_repetitions)
        #
        # self.checkBox_weight.setChecked(False)
        # self.checkBox_body_weight.setChecked(False)
        # if tex.baseline_weight:
        #     self.checkBox_weight.setChecked(True)
        #     self.doubleSpinBox_weight.setValue(tex.baseline_weight)
        # if tex.tex_usr_id:
        #     self.checkBox_weight.setChecked(True)
        #     self.checkBox_body_weight.setChecked(True)
        #     self.doubleSpinBox_weight.setValue(self.usr.weight)
        # if tex.baseline_duration:
        #     self.checkBox_duration.setChecked(True)
        #     self.doubleSpinBox_duration.setValue(tex.baseline_duration)

    def import_exercise_clicked(self):

        exercise = self.listWidget_exercise.currentItem()

        if exercise:
            # Add the a new relation
            self.import_exercise()
