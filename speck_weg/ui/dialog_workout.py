# fingertraining
# Stefan Hochuli, 22.07.2021,
# Folder: speck_weg/ui File: dialog_workout.py
#

from typing import Optional, TYPE_CHECKING

from PyQt5.QtWidgets import QDialog

from .dialog_workout_ui import Ui_Dialog_workout
from .messages import open_message_box
from ..app.workout import Workout

if TYPE_CHECKING:
    from ..db import CRUD
    from ..models import TrainingExerciseModel, WorkoutExerciseModel


class WorkoutDialog(Workout, QDialog, Ui_Dialog_workout):

    def __init__(self,
                 # Workout
                 db: 'CRUD', tpr: int = None, wse: int = None,
                 # Qdialog
                 parent=None,
                 ):
        # With super, the arguments for the QDialog (second inheritance)
        # must be passed in the __init__ function of Workout (first inheritance)
        super().__init__(db=db, tpr=tpr, wse=wse,
                         parent=parent)

        # Workout is initialized, if a user is missing, open messagebox
        # -> move to main window -> cant start a workout without a user

        self.setupUi(self)
        self.connect()

        self.update_dialog()

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_save.clicked.connect(self.save_clicked)
        self.pushButton_delete.clicked.connect(self.delete_clicked)
        self.pushButton_previous_exercise.clicked.connect(self.previous_exercise_clicked)
        self.pushButton_next_exercise.clicked.connect(self.next_exercise_clicked)
        # not working properly, use separate functions
        # self.pushButton_start.clicked.connect(lambda: self.previous_exercise(-1))
        # self.pushButton_end.clicked.connect(lambda: self.next_exercise(len(self.exercises)))

        self.doubleSpinBox_weight.valueChanged.connect(self.weight_changed)
        self.doubleSpinBox_ratio.valueChanged.connect(self.ratio_changed)

    def save_clicked(self):
        # update wse / wex objects from widgets
        self.save(repetitions=self.spinBox_repetitions.value(),
                  weight=self.doubleSpinBox_weight.value(),
                  duration=self.doubleSpinBox_duration.value(),
                  comment=self.textEdit_comment.toPlainText())

        # update everything? only assessment changes...
        score = self.assess()
        self.assess_set_text(score)

    def delete_clicked(self):
        # if self.current_pos == -1 or self.current_pos == len(self.exercises):
        if self.delete_message:
            # start or end, delete the session and all exercises
            message = self.messages['delete_session']
            clicked = open_message_box(message)
            if clicked:
                self.delete()
                self.reject()

        else:
            # Delete an exercise or an empty session
            self.delete()

    def previous_exercise_clicked(self):
        print('previous exercise')
        # minimum position: -1

        self.previous_exercise()
        self.update_dialog()

    def next_exercise_clicked(self):
        print('next exercise')
        # maximum position: len(self.exercises)

        self.next_exercise()

        self.update_dialog()

    def weight_changed(self):
        # weight was changed --> update the ratio
        ratio = self.calc_ratio(self.doubleSpinBox_weight.value())
        self.doubleSpinBox_ratio.setValue(ratio)

    def ratio_changed(self):
        # ratio was changed --> update the weight
        weight = self.calc_weight(self.doubleSpinBox_ratio.value())
        self.doubleSpinBox_weight.setValue(weight)

    def update_dialog(self):

        # self.update_baseline()
        print('update dialog')
        start = self.start_position
        end = self.end_position

        self.update_labels()

        if not start and not end:
            self.set_values()

        score = self.assess()
        self.assess_set_text(score)

    def update_labels(self):
        print('update labels')
        # set labels and activate/deactivate widgets

        # Enable all  input and buttons
        self.spinBox_repetitions.setEnabled(True)
        self.doubleSpinBox_weight.setEnabled(True)
        self.doubleSpinBox_ratio.setEnabled(True)
        self.doubleSpinBox_duration.setEnabled(True)
        self.textEdit_comment.setEnabled(True)
        self.pushButton_previous_exercise.setEnabled(True)
        self.pushButton_next_exercise.setEnabled(True)
        self.pushButton_start.setEnabled(True)
        self.pushButton_end.setEnabled(True)
        self.pushButton_save.setEnabled(True)
        self.pushButton_delete.setEnabled(True)

        tpr = self.workout_session.tpr_model
        self.label_program.setText(
            f'{tpr.training_theme.name}: {tpr.name}'
        )
        if self.start_position:
            print('  setting start')
            self.label_exercise.setText('Start')
            self.label_sets.setText('')
            # enable / disable buttons / input
            self.spinBox_repetitions.setEnabled(False)
            self.doubleSpinBox_weight.setEnabled(False)
            self.doubleSpinBox_ratio.setEnabled(False)
            self.doubleSpinBox_duration.setEnabled(False)
            self.pushButton_previous_exercise.setEnabled(False)
            self.pushButton_start.setEnabled(False)
            # update widgets
            self.textEdit_comment.setText(self.workout_session.model.comment)

        elif self.end_position:

            print('  setting end')
            self.label_exercise.setText('Ende')
            self.label_sets.setText('')
            # enable / disable buttons / input
            self.spinBox_repetitions.setEnabled(False)
            self.doubleSpinBox_weight.setEnabled(False)
            self.doubleSpinBox_ratio.setEnabled(False)
            self.doubleSpinBox_duration.setEnabled(False)
            self.pushButton_next_exercise.setEnabled(False)
            self.pushButton_end.setEnabled(False)
            # update widgets
            self.textEdit_comment.setText(self.workout_session.model.comment)

        else:
            # Exercise
            print('  setting exercise')
            tex, wex = self.current_tex_wex
            # Add the information from the current tex and wex
            self.label_exercise.setText(tex.name)
            self.label_sets.setText(f'Set {self.current_set + 1} / {tex.baseline_sets}')

            if not self.current_exercise_set.baseline_weight:
                self.doubleSpinBox_weight.setEnabled(False)
                self.doubleSpinBox_ratio.setEnabled(False)
            if not tex.baseline_duration:
                self.doubleSpinBox_duration.setEnabled(False)

    def set_values(self):
        print('set values')
        tex, wex = self.current_tex_wex

        if wex:  # load the existing workout exercise
            # Set the values based on the existing workout exercise
            self.set_wex_values(wex, self.current_exercise_set.baseline_weight)

        else:  # set the default values of the training exercise
            self.set_default_values(tex, self.current_exercise_set.baseline_weight)

    def set_wex_values(self, wex: 'WorkoutExerciseModel', baseline_weight: float):
        print(wex.repetitions, wex.weight, wex.comment)
        self.spinBox_repetitions.setValue(wex.repetitions)
        if wex.weight:
            self.doubleSpinBox_weight.setValue(wex.weight)
            self.doubleSpinBox_ratio.setValue(wex.weight / baseline_weight)
        else:  # should not happen
            self.doubleSpinBox_weight.clear()
            self.doubleSpinBox_ratio.clear()
        if wex.duration:
            self.doubleSpinBox_duration.setValue(wex.duration)
        else:  # should not happpen
            self.doubleSpinBox_duration.clear()

        self.textEdit_comment.setText(wex.comment)

    def set_default_values(self, tex: 'TrainingExerciseModel', baseline_weight: float):
        print(tex.baseline_repetitions, tex.baseline_weight, tex.baseline_duration)
        print(baseline_weight, tex.baseline_duration)
        self.spinBox_repetitions.setValue(tex.baseline_repetitions)
        if baseline_weight:  # tex.baseline_weight or usr.weight
            self.doubleSpinBox_weight.setValue(baseline_weight)
            self.doubleSpinBox_ratio.setValue(1)
        else:
            self.doubleSpinBox_weight.clear()
            self.doubleSpinBox_ratio.clear()
        if tex.baseline_duration:  # tex.baseline_duration
            self.doubleSpinBox_duration.setValue(tex.baseline_duration)
        else:
            self.doubleSpinBox_duration.clear()
        self.textEdit_comment.clear()  # no comment yet

    def assess_set_text(self, score: Optional[float]):
        if score == float(0):
            # invalid session, no exercices yet
            self.lineEdit_assessment.setText('Noch keine Übungen gespeichert.')
        elif score:
            # Valid score (session or exercise)
            self.lineEdit_assessment.setText(f'{score*100:.2f} %')
        else:
            # invalid exercise, not saved yet
            self.lineEdit_assessment.setText('Noch nicht gespeichert')
