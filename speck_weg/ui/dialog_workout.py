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
        self.baseline_weight: Optional[float] = None
        self.baseline_duration: Optional[float] = None

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
        self.exercises = [
            [tpe.training_exercise, None] for tpe in self.parent_tpr.training_exercises
        ]
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

        self.doubleSpinBox_weight.valueChanged.connect(self.weight_changed)
        self.doubleSpinBox_ratio.valueChanged.connect(self.ratio_changed)

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
        try:
            tex, wex = self.current_exercise
            print('saving exercise')

            if wex:
                print('  existing', wex)
                # The exercise already exists in the database
                wex.repetitions = self.spinBox_repetitions.value()
                wex.weight = self.doubleSpinBox_weight.value()
                wex.description = self.textEdit_comment.toPlainText()

                self.db.update()

            else:
                print('  new wex')
                print('wse', self.wse.wse_id)
                print('tex', tex.tex_id)
                print(self.spinBox_repetitions.value())
                print(self.doubleSpinBox_weight.value(), self.doubleSpinBox_ratio.value())
                print('object:')

                if self.baseline_weight:
                    weight = self.doubleSpinBox_weight.value() * self.doubleSpinBox_ratio.value()
                else:
                    weight = None
                if self.baseline_duration:
                    duration = self.doubleSpinBox_duration.value()
                else:
                    duration = None
                # if weight < 5:
                #     # ratio given, not weight in kg
                #     ratio = weight
                #     weight = ratio * self.usr.weight
                # else:
                #     # kg given
                #     ratio = weight / self.usr.weight

                wex = WorkoutExercise(
                    wex_wse_id=self.wse.wse_id,
                    wex_tex_id=tex.tex_id,
                    repetitions=self.spinBox_repetitions.value(),
                    weight=weight,
                    duration=duration
                )
                print(' ', wex)
                self.db.create(wex)

            # update-statement in the commit if wex already exists, else insert
            # print('  committing', self.db.session.dirty, self.db.session.new)
            # self.db.session.commit()
            # print('tex added to the database')

            # Add the tex to the wex
            self.current_exercise[1] = wex
            print(self.current_exercise)

            # Clear after saving for adding a new one
            # self.lineEdit_name.clear()
            # self.lineEdit_description.clear()
            # print('cleared')

        except Exception as exc:
            print(exc)
            raise exc

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

    def weight_changed(self):
        # weight was changed --> update the ratio
        # self.doubleSpinBox_ratio.setValue(self.doubleSpinBox_weight.value() / self.usr.weight)
        # recalculate the ratio if the weight is changed

        ratio = self.doubleSpinBox_weight.value() / self.baseline_weight
        self.doubleSpinBox_ratio.setValue(ratio)

    def ratio_changed(self):
        # ratio was changed --> update the weight

        weight = self.doubleSpinBox_ratio.value() * self.baseline_weight
        self.doubleSpinBox_weight.setValue(weight)

    def update_labels(self):
        print('update labels')
        # set labels and activate/deactivate widgets

        # Enable all  input and buttons
        self.spinBox_repetitions.setEnabled(True)
        self.doubleSpinBox_weight.setEnabled(True)
        self.doubleSpinBox_ratio.setEnabled(True)
        self.doubleSpinBox_duration.setEnabled(True)
        self.textEdit_comment.setEnabled(True)
        self.pushButton_previous.setEnabled(True)
        self.pushButton_next.setEnabled(True)
        self.pushButton_save_exercise.setEnabled(True)

        if self.current_pos <= -1:
            self.current_pos = -1
            print('  setting start')
            self.label_exercise.setText('Start')
            # enable / disable buttons / input
            self.spinBox_repetitions.setEnabled(False)
            self.doubleSpinBox_weight.setEnabled(False)
            self.doubleSpinBox_ratio.setEnabled(False)
            self.doubleSpinBox_duration.setEnabled(False)
            self.pushButton_previous.setEnabled(False)
            # update widgets
            self.textEdit_comment.setText(self.wse.comment)

        elif self.current_pos >= len(self.exercises):
            print('  setting end')
            self.label_exercise.setText('Ende')
            self.current_pos = len(self.exercises)
            # enable / disable buttons / input
            self.spinBox_repetitions.setEnabled(False)
            self.doubleSpinBox_weight.setEnabled(False)
            self.doubleSpinBox_ratio.setEnabled(False)
            self.doubleSpinBox_duration.setEnabled(False)
            self.pushButton_next.setEnabled(False)
            # update widgets
            self.textEdit_comment.setText(self.wse.comment)
        else:
            print('  setting exercise')
            # Add the information from the current tex and wex
            print(' ', self.current_exercise)
            tex, wex = self.current_exercise
            # set default values for weight / duration
            if tex.baseline_weight:
                self.baseline_weight = tex.baseline_weight
            elif tex.tex_usr_id:
                self.baseline_weight = self.usr.weight
            else:
                self.baseline_weight = None
            if tex.baseline_duration:
                self.baseline_duration = tex.baseline_duration
            else:
                self.baseline_duration = None

            self.label_exercise.setText(tex.name)
            if not self.baseline_weight:
                self.doubleSpinBox_weight.setEnabled(False)
                self.doubleSpinBox_ratio.setEnabled(False)
            if not self.baseline_duration:
                self.doubleSpinBox_duration.setEnabled(False)

    def update_dialog(self):
        print('update dialog')
        self.update_labels()
        try:
            if self.current_pos in range(0, len(self.exercises)):
                self.set_values()
        except Exception as exc:
            print(exc)
            raise

    def set_values(self):
        print('set values')
        # if self.doubleSpinBox_weight.isEnabled():
        tex, wex = self.current_exercise

        if wex:  # load the existing workout exercise
            # Set the values based on the existing workout exercise
            print(wex.repetitions, wex.weight, wex.comment)
            self.spinBox_repetitions.setValue(wex.repetitions)
            if wex.weight:
                self.doubleSpinBox_weight.setValue(wex.weight)
                self.doubleSpinBox_ratio.setValue(wex.weight / self.baseline_weight)
            else:  # should not happen
                self.doubleSpinBox_weight.clear()
                self.doubleSpinBox_ratio.clear()
            if wex.duration:
                self.doubleSpinBox_duration.setValue(wex.duration)
            else:  # should not happpen
                self.doubleSpinBox_duration.clear()

            self.textEdit_comment.setText(wex.comment)

        else:  # set the default values of the training exercise
            print(tex.baseline_repetitions, tex.baseline_weight, tex.baseline_duration)
            print(self.baseline_weight, self.baseline_duration)
            self.spinBox_repetitions.setValue(tex.baseline_repetitions)
            if self.baseline_weight:  # tex.baseline_weight or usr.weight
                self.doubleSpinBox_weight.setValue(self.baseline_weight)
                self.doubleSpinBox_ratio.setValue(1)
            else:
                self.doubleSpinBox_weight.clear()
                self.doubleSpinBox_ratio.clear()
            if self.baseline_duration:  # tex.baseline_duration
                self.doubleSpinBox_duration.setValue(self.baseline_duration)
            else:
                self.doubleSpinBox_duration.clear()
            self.textEdit_comment.clear()  # no comment yet

    @property
    def current_exercise(self) -> Union[List, None]:
        if self.current_pos in range(len(self.exercises)):
            return self.exercises[self.current_pos]
        else:
            print('out of range', self.current_pos, len(self.exercises))
            return None
