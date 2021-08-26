# fingertraining
# Stefan Hochuli, 20.07.2021,
# Folder: speck_weg/ui File: dialog_training_exercise.py
#


from typing import TYPE_CHECKING, Optional

from PyQt5.QtWidgets import QDialog
import PyQt5.QtCore

from ..models import TrainingExercise
from .dialog_training_exercise_ui import Ui_Dialog_training_exercise

if TYPE_CHECKING:
    from ..db import CRUD
    from ..models import TrainingProgram, User


user_role = PyQt5.QtCore.Qt.UserRole


class ExerciseDialog(QDialog, Ui_Dialog_training_exercise):

    tex: Optional['TrainingExercise'] = None
    # max_sequence: int = 0  # ordering sequence for the exercises, starting from 1

    def __init__(self, db: 'CRUD', parent=None,
                 obj: 'TrainingExercise' = None, parent_tpr: 'TrainingProgram' = None,
                 usr: 'User' = None):
        super().__init__(parent)

        self.db = db

        self.tex = obj
        self.parent_tpr = parent_tpr
        self.usr = usr

        self.setupUi(self)
        self.connect()

        # previous / next not ready yet
        self.pushButton_next.setEnabled(False)
        self.pushButton_previous.setEnabled(False)

        if self.tex:
            self.lineEdit_name.setText(self.tex.name)
            self.lineEdit_description.setText(self.tex.description)
            self.spinBox_repetitions.setValue(self.tex.repetitions)

            if self.tex.weight:
                if self.tex.tex_usr_id:
                    self.doubleSpinBox_weight.setValue(self.usr.weight)
                else:
                    self.doubleSpinBox_weight.setValue(self.tex.weight)
            if self.tex.duration:
                self.doubleSpinBox_duration.setValue(self.tex.duration)
        #     print('edit mode')
        #     self.set_edit_mode()
        #     # self.sequence = self.tex.sequence
        # else:
        #     print('new mode')
        #     # self.max_sequence += 1
        #     self.set_new_mode()

    @property
    def max_sequence(self) -> int:
        if self.parent_tpr.training_exercises:
            return max([tex.sequence for tex in self.parent_tpr.training_exercises])
        else:
            return 0

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_previous.clicked.connect(self.previous_exercise)
        self.pushButton_next.clicked.connect(self.next_exercise)

    def save(self):
        # Return the object, add to the db from main window
        if self.tex:
            print('editing')
            self.update_object()

            self.db.update()

        else:
            print('new tex')

            try:
                self.tex = TrainingExercise()
                # self.tex = TrainingExercise(
                #     name=self.lineEdit_name.text(),
                #     description=self.lineEdit_description.text(),
                #     baseline_repetitions=self.spinBox_repetitions.value(),
                # )

                self.update_object()

                self.tex.sequence = self.max_sequence + 1
                self.tex.training_programs.append(self.parent_tpr)

                self.db.create(self.tex)
                print('tex added to the database')
            except Exception as exc:
                print(exc)
                raise

        # Clear after saving for adding a new one
        self.lineEdit_name.clear()
        self.lineEdit_description.clear()
        # self.spinBox_repetitions.clear()
        # self.doubleSpinBox_duration.clear()
        # Reset the focus on the first lineEdit
        self.lineEdit_name.setFocus()
        self.tex = None

    def previous_exercise(self):
        pass

    def next_exercise(self):
        pass

    def update_object(self):
        if self.tex:
            self.tex.name = self.lineEdit_name.text()
            self.tex.description = self.lineEdit_description.text()
            self.tex.baseline_repetitions = self.spinBox_repetitions.value()
            if self.checkBox_weight.isChecked():
                print('weight')
                if self.checkBox_body_weight.isChecked():
                    print('body weight')
                    self.tex.tex_usr_id = self.usr.usr_id
                else:
                    print('custom weight')
                    self.tex.baseline_weight = self.doubleSpinBox_weight.value()
            if self.checkBox_duration.isChecked():
                print('duration')
                self.tex.baseline_duration = self.doubleSpinBox_duration.value()
        else:
            raise ValueError('No Training program object for updating.')

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
