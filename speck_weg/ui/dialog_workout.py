# fingertraining
# Stefan Hochuli, 22.07.2021,
# Folder: speck_weg/ui File: dialog_workout.py
#

from typing import Optional, TYPE_CHECKING

from PyQt5.QtWidgets import QDialog

from .dialog_workout_ui import Ui_Dialog_workout
from .messages import open_message_box
from ..app import Workout

if TYPE_CHECKING:
    from ..db import CRUD
    from ..models import TrainingProgramModel, TrainingExerciseModel, WorkoutSessionModel, WorkoutExerciseModel


class WorkoutDialog(Workout, QDialog, Ui_Dialog_workout):

    def __init__(self,
                 # Workout
                 db: 'CRUD', parent_tpr: 'TrainingProgramModel', obj: 'WorkoutSessionModel' = None,
                 # Qdialog
                 parent=None,
                 ):
        # With super, the arguments for the QDialog (second inheritance)
        # must be passed in the __init__ function of Workout (first inheritance)
        super().__init__(db=db, parent_tpr=parent_tpr, obj=obj,
                         parent=parent)

        # Workout is initialized, if a user is missing, open messagebox
        if not self.usr:
            message = self.messages['no_user']
            open_message_box(message)

        self.setupUi(self)
        self.connect()

        self.update_dialog(start=True)

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
        if self.current_pos == -1 or self.current_pos == len(self.exercises):
            # start or end, delete the session
            message = self.messages['delete_session']
            clicked = open_message_box(message)
            if clicked:
                self.delete()
                self.reject()

            # self.db.delete(self.wse)
        else:
            # Delete an exercise
            self.delete()

    def previous_exercise_clicked(self):
        print('previous exercise')
        # minimum position: -1

        previous_ex = self.previous_exercise()
        print(previous_ex)

        if previous_ex == 'start':
            self.update_dialog(start=True)
        else:
            tex, wex = previous_ex
            self.update_dialog(tex=tex, wex=wex)

    def next_exercise_clicked(self):
        print('next exercise')
        # maximum position: len(self.exercises)

        next_ex = self.next_exercise()
        print(next_ex)

        if next_ex == 'end':
            self.update_dialog(end=True)
        else:
            tex, wex = next_ex
            self.update_dialog(tex=tex, wex=wex)

    def weight_changed(self):
        # weight was changed --> update the ratio
        ratio = self.calc_ratio(self.doubleSpinBox_weight.value())
        self.doubleSpinBox_ratio.setValue(ratio)

    def ratio_changed(self):
        # ratio was changed --> update the weight
        weight = self.calc_weight(self.doubleSpinBox_ratio.value())
        self.doubleSpinBox_weight.setValue(weight)

    def update_dialog(self, start=False, end=False, tex=None, wex=None):

        self.update_baseline()
        print('update dialog')
        self.update_labels(start, end, tex)

        if tex:
            self.set_values(tex, wex)

        score = self.assess()
        self.assess_set_text(score)

    def update_labels(self, start: bool = False, end: bool = False,
                      tex: 'TrainingExerciseModel' = None):
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

        self.label_program.setText(
            f'{self.parent_tpr.training_theme.name}: {self.parent_tpr.name}'
        )
        if start:
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
            self.textEdit_comment.setText(self.wse.comment)

        elif end:
            self.current_pos = len(self.exercises)
            self.baseline_weight = None
            self.baseline_duration = None

            print('  setting end')
            self.label_exercise.setText('Ende')
            self.label_sets.setText('')
            self.current_pos = len(self.exercises)
            # enable / disable buttons / input
            self.spinBox_repetitions.setEnabled(False)
            self.doubleSpinBox_weight.setEnabled(False)
            self.doubleSpinBox_ratio.setEnabled(False)
            self.doubleSpinBox_duration.setEnabled(False)
            self.pushButton_next_exercise.setEnabled(False)
            self.pushButton_end.setEnabled(False)
            # update widgets
            self.textEdit_comment.setText(self.wse.comment)

        elif tex:
            print('  setting exercise')
            # Add the information from the current tex and wex
            self.label_exercise.setText(tex.name)
            self.label_sets.setText(f'Set {self.current_set} / {tex.baseline_sets}')

            if not self.baseline_weight:
                self.doubleSpinBox_weight.setEnabled(False)
                self.doubleSpinBox_ratio.setEnabled(False)
            if not self.baseline_duration:
                self.doubleSpinBox_duration.setEnabled(False)

    def set_values(self, tex: 'TrainingExerciseModel', wex: 'WorkoutExerciseModel'):
        print('set values')

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
