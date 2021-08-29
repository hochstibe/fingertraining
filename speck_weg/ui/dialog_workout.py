# fingertraining
# Stefan Hochuli, 22.07.2021,
# Folder: speck_weg/ui File: dialog_workout.py
#

from typing import List, Optional, Union, TYPE_CHECKING

from PyQt5.QtWidgets import QDialog, QMessageBox

from ..models import WorkoutSession, WorkoutExercise, TrainingExercise, User
from .dialog_workout_ui import Ui_Dialog_workout

if TYPE_CHECKING:
    from ..db import CRUD
    from ..models import TrainingProgram


class WorkoutDialog(QDialog, Ui_Dialog_workout):

    wse: 'WorkoutSession' = None
    usr: 'User' = None

    def __init__(self, db: 'CRUD', parent=None,
                 obj: 'WorkoutSession' = None, parent_tpr: 'TrainingProgram' = None):
        super().__init__(parent)

        self.db = db

        self.wse = obj
        self.parent_tpr = parent_tpr

        self.setupUi(self)
        self.connect()

        # Get the current user
        self.usr = self.db.read_first(User)
        if not self.usr:

            print('No program selected')
            msg = QMessageBox()

            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('Kein User angegeben')
            msg.setText('Bitte zuerst das Gewicht eingeben.')
            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec()

        # List of [index, planned exercise, logged exercise
        self.exercises: List[List['TrainingExercise', Optional[WorkoutExercise]]] = []
        self.current_pos: int = -1

        # Add the form layout to a frame (

        if self.wse:
            # edit mode
            pass
        else:
            # new mode
            self.wse = WorkoutSession(wse_tpr_id=self.parent_tpr.tpr_id)
            # Commit the workout session with the first exercise
            self.db.create(self.wse)

        # Generate a list for all exercises (pairs for planned an done exercises
        self.exercises = [[tex, None] for tex in self.parent_tpr.training_exercises]
        # self.exercises.insert(0, [0, None, None])
        # self.exercises.append([len(self.exercises), None, None])
        print('exercises:')
        print(self.exercises)

        self.update_dialog()

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_save_exercise.clicked.connect(self.save)
        self.pushButton_previous.clicked.connect(self.previous_exercise)
        self.pushButton_next.clicked.connect(self.next_exercise)

        self.doubleSpinBox_weight.valueChanged.connect(self.update_ratio)
        self.doubleSpinBox_ratio.valueChanged.connect(self.update_weight)

    def save(self):
        if self.current_pos == -1:
            self.save_session()
        elif self.current_pos == len(self.exercises):
            self.save_session()
        else:
            self.save_exercise()

    def save_session(self):
        print('saving session (comment)')
        # save the comment
        print(self.wse, self.textEdit_comment.toPlainText())
        self.wse.comment = self.textEdit_comment.toPlainText()
        print(self.wse)
        print('dirty', self.wse in self.db.session.dirty)
        self.db.update()
        print('dirty', self.wse in self.db.session.dirty)

    def save_exercise(self):
        # Return the object, add to the db from main window

        tex, wex = self.current_exercise
        print('saving exercise')

        if wex:
            print('  existing', wex)
            # The exercise already exists in the database
            wex.repetitions = self.spinBox_repetitions.value()
            wex.weight = self.doubleSpinBox_weight.value()
            wex.description = self.textEdit_comment.text()
        else:
            print('  new wex')
            print('wse', self.wse.wse_id)
            print('tex', tex.tex_id)
            print(self.spinBox_repetitions.value())
            print(self.doubleSpinBox_weight.value(), self.doubleSpinBox_ratio.value())
            print('object:')
            try:
                weight = self.doubleSpinBox_weight.value()
                if weight < 5:
                    # ratio given, not weight in kg
                    ratio = weight
                    weight = ratio * self.usr.weight
                else:
                    # kg given
                    ratio = weight / self.usr.weight

                wex = WorkoutExercise(
                    wex_wse_id=self.wse.wse_id,
                    wex_tex_id=tex.tex_id,
                    repetitions=self.spinBox_repetitions.value(),
                    weight=weight,
                    ratio=ratio
                )
                print(' ', wex)
            except Exception as exc:
                print(exc)
                raise exc
            self.db.create(wex)

        # update-statement in the commit if wex already exists, else insert
        print('  committing', self.db.session.dirty, self.db.session.new)
        self.db.session.commit()
        print('tex added to the database')

        # Add the tex to the wex
        self.current_exercise[1] = wex
        print(self.current_exercise)

        # Clear after saving for adding a new one
        # self.lineEdit_name.clear()
        # self.lineEdit_description.clear()
        # print('cleared')

    def previous_exercise(self):
        print('previous exercise')
        # minimum position: -1
        if self.current_pos > -1:
            self.current_pos -= 1
        self.update_dialog()

    def next_exercise(self):
        print('next exercise')
        # maximum position: len(self.exercises)
        if self.current_pos < len(self.exercises):
            self.current_pos += 1
        self.update_dialog()

    def update_ratio(self):
        # weight was changed --> update the ratio
        self.doubleSpinBox_ratio.setValue(self.doubleSpinBox_weight.value() / self.usr.weight)

    def update_weight(self):
        # ratio was changed --> update the weight
        self.doubleSpinBox_weight.setValue(self.doubleSpinBox_ratio.value() * self.usr.weight)

    def update_dialog(self):

        # Enable all  input and buttons
        self.spinBox_repetitions.setReadOnly(False)
        self.doubleSpinBox_weight.setReadOnly(False)
        self.doubleSpinBox_ratio.setReadOnly(False)
        self.textEdit_comment.setReadOnly(False)
        self.pushButton_previous.setEnabled(True)
        self.pushButton_next.setEnabled(True)
        self.pushButton_save_exercise.setEnabled(True)

        print('updating', self.current_pos)
        if self.current_pos == -1:
            print('  setting start')
            self.label_exercise.setText('Start')
            # enable / disable buttons / input
            self.spinBox_repetitions.setReadOnly(True)
            self.doubleSpinBox_weight.setReadOnly(True)
            self.doubleSpinBox_ratio.setReadOnly(True)
            self.textEdit_comment.setReadOnly(False)
            self.pushButton_previous.setEnabled(False)
            self.pushButton_next.setEnabled(True)
            self.pushButton_save_exercise.setEnabled(True)

            self.textEdit_comment.setText(self.wse.comment)

        elif self.current_pos >= len(self.exercises):
            print('  setting end')
            self.label_exercise.setText('Ende')
            self.current_pos = len(self.exercises)
            # enable / disable buttons / input
            self.spinBox_repetitions.setReadOnly(True)
            self.doubleSpinBox_weight.setReadOnly(True)
            self.doubleSpinBox_ratio.setReadOnly(True)
            self.textEdit_comment.setReadOnly(False)
            self.pushButton_previous.setEnabled(True)
            self.pushButton_next.setEnabled(False)
            self.pushButton_save_exercise.setEnabled(True)

            self.textEdit_comment.setText(self.wse.comment)
        else:
            print('  setting exercise')
            # Add the information from the current tex and wex
            print(' ', self.current_exercise)
            tex, wex = self.current_exercise
            print('    setting labels')
            self.label_exercise.setText(tex.name)
            # enable / disable buttons / input
            self.pushButton_previous.setEnabled(True)
            self.pushButton_next.setEnabled(True)
            self.pushButton_save_exercise.setEnabled(True)

            if wex:
                print(wex.repetitions, wex.weight, wex.comment)
                self.spinBox_repetitions.setValue(wex.repetitions)
                self.doubleSpinBox_weight.setValue(wex.weight)
                self.doubleSpinBox_ratio.setValue(wex.ratio)
                self.textEdit_comment.setText(wex.comment)
            else:
                print('clearing labels')
                # Set default values for spinboxes
                # Todo: default value in tex datamodel
                self.spinBox_repetitions.setValue(1)
                self.doubleSpinBox_weight.setValue(self.usr.weight)
                self.doubleSpinBox_ratio.setValue(1)
                self.textEdit_comment.clear()
                print('cleared')

    @property
    def current_exercise(self) -> Union[List, None]:
        if self.current_pos in range(len(self.exercises)):
            return self.exercises[self.current_pos]
        else:
            print('out of range', self.current_pos, len(self.exercises))
            return None
