# fingertraining
# Stefan Hochuli, 22.07.2021,
# Folder: speck_weg/ui File: dialog_workout.py
#

from typing import List, Tuple, Optional, Union, TYPE_CHECKING

from PyQt5.QtWidgets import QDialog

from ..models import WorkoutSession, WorkoutExercise, TrainingExercise, User
from .dialog_workout_ui import Ui_Dialog_workout
from .messages import open_message_box

if TYPE_CHECKING:
    from ..db import CRUD
    from ..models import TrainingProgram


class WorkoutDialog(QDialog, Ui_Dialog_workout):

    def __init__(self, db: 'CRUD', parent=None,
                 obj: 'WorkoutSession' = None, parent_tpr: 'TrainingProgram' = None):
        super().__init__(parent)

        self.db = db

        self.wse: Optional['WorkoutSession'] = obj
        self.parent_tpr: 'TrainingProgram' = parent_tpr
        # List of [planned exercise, [logged sets of the exercise]]
        self.exercises: List[List['TrainingExercise', List[Optional[WorkoutExercise]]]] = []

        self.setupUi(self)
        self.connect()

        # Get the current user
        self.usr: 'User' = self.db.read_first(User)
        if not self.usr:

            print('No program selected')
            title = 'Kein Programm ausgewählt.'
            text = 'Bitte zuerst ein Programm auswählen und anschliessend das Workout starten.'
            open_message_box(title, text, 'information')

        self.current_pos: int = -1
        self.current_set: int = -1
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
            [tpe.training_exercise, [None for _ in range(tpe.training_exercise.baseline_sets)]]
            for tpe in self.parent_tpr.training_exercises
        ]
        # self.exercises.insert(0, [0, None, None])
        # self.exercises.append([len(self.exercises), None, None])
        print('exercises:')
        print(self.exercises)

        self.update_dialog()

    @property
    def current_exercise(self) -> Union[
        Tuple['TrainingExercise', Optional['WorkoutExercise']],
        None
    ]:
        """
        :return: Current TrainingExercise,  current WorkoutExercise (if already saved)
        """
        if self.current_pos in range(len(self.exercises)):
            tex, wexes = self.exercises[self.current_pos]
            wex = wexes[self.current_set - 1]
            print(tex, wex)
            return tex, wex
        else:
            print('out of range', self.current_pos, len(self.exercises))
            return None

    @current_exercise.setter
    def current_exercise(self, wex: 'WorkoutExercise'):
        if self.current_pos in range(len(self.exercises)):
            tex, wexes = self.exercises[self.current_pos]
            wexes[self.current_set - 1] = wex

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_delete.clicked.connect(self.delete)
        self.pushButton_previous_exercise.clicked.connect(self.previous_exercise)
        self.pushButton_next_exercise.clicked.connect(self.next_exercise)
        self.pushButton_start.clicked.connect(self.previous_exercise, -1)
        self.pushButton_end.clicked.connect(self.next_exercise, len(self.exercises))

        self.doubleSpinBox_weight.valueChanged.connect(self.weight_changed)
        self.doubleSpinBox_ratio.valueChanged.connect(self.ratio_changed)

    def save(self):
        if self.current_pos == -1:
            # start
            self.save_session()
        elif self.current_pos == len(self.exercises):
            # stop
            self.save_session()
        else:
            self.save_exercise()

    def delete(self):
        if self.current_pos == -1 or self.current_pos == len(self.exercises):
            # start or end
            title = 'Session löschen'
            text = 'Die Session wird geschlossen und gelöscht. ' \
                   'Alle gespeicherten Übungen werden ebenfalls gelöscht.'
            clicked = open_message_box(title, text, 'question',
                                       button_accept_name='Löschen')
            if clicked:
                if self.wse.workout_exercises:
                    self.db.delete(self.wse.workout_exercises)
                self.db.delete(self.wse)
                self.reject()

            # self.db.delete(self.wse)
        else:
            tex, wex = self.current_exercise
            self.db.delete(wex)

    def save_session(self):
        print('saving session (comment)')
        # save the comment
        print(self.wse, self.textEdit_comment.toPlainText())
        self.wse.comment = self.textEdit_comment.toPlainText()
        print(self.wse)
        print('dirty', self.wse in self.db.session.dirty)
        self.db.update()
        print('dirty', self.wse in self.db.session.dirty)

        score = self.assess_session()
        self.assess_session_set_text(score)

    def save_exercise(self):
        # Return the object, add to the db from main window
        tex, wex = self.current_exercise
        print('saving exercise')

        if wex:
            print('  existing', wex)
            # The exercise already exists in the database
            wex.set = self.current_set
            wex.repetitions = self.spinBox_repetitions.value()
            if self.baseline_weight:
                wex.weight = self.doubleSpinBox_weight.value()
            if self.baseline_duration:
                wex.duration = self.doubleSpinBox_duration.value()
            wex.description = self.textEdit_comment.toPlainText()

            self.db.update()

        else:
            if self.baseline_weight:
                weight = self.doubleSpinBox_weight.value() * self.doubleSpinBox_ratio.value()
            else:
                weight = None
            if self.baseline_duration:
                duration = self.doubleSpinBox_duration.value()
            else:
                duration = None

            wex = WorkoutExercise(
                wex_wse_id=self.wse.wse_id,
                wex_tex_id=tex.tex_id,
                sequence=self.current_pos + 1,  # the position equals the sequence in the tpe
                set=self.current_set,
                repetitions=self.spinBox_repetitions.value(),
                weight=weight,
                duration=duration
            )
            print(' ', wex)
            self.db.create(wex)

        # Add the tex to the wex
        self.current_exercise = wex
        print(self.current_exercise)

        # assess the score of the exercise
        score = self.assess_exercise(tex, wex)
        self.assess_exercise_set_text(score)

    def previous_exercise(self, goto: int = None):
        print('previous exercise')
        # minimum position: -1
        if goto:
            self.current_pos = goto + 1

        if len(self.exercises) == self.current_pos:
            # end position, go to last set of the last exercise, current_set was not changed
            self.current_pos -= 1
            tex, wex = self.current_exercise
            self.current_set = tex.baseline_sets

        elif 0 == self.current_pos:
            if self.current_set == 1:
                # go to start position
                self.current_pos -= 1
            else:
                self.current_set -= 1

        elif self.current_pos > -1:
            if self.current_set > 1:
                # previous set of the current exercise
                print('previous set of the current exercise')
                self.current_set -= 1
            else:
                # last set of the previous exercise
                print('last set of the previous exercise')
                self.current_pos -= 1
                tex, wex = self.current_exercise
                self.current_set = tex.baseline_sets

        self.update_dialog()

    def next_exercise(self, goto: int = None):
        print('next exercise')
        # maximum position: len(self.exercises)
        if goto:
            self.current_pos = goto - 1

        if self.current_pos == len(self.exercises) - 1:
            tex, wex = self.current_exercise
            if self.current_set == tex.baseline_sets:
                # go to end position
                self.current_pos += 1
            else:
                self.current_set += 1

        elif -1 == self.current_pos:
            # start position, go to first set of the first exercise
            self.current_pos += 1
            self.current_set = 1
        elif self.current_pos < len(self.exercises):
            tex, wex = self.current_exercise
            if self.current_set < tex.baseline_sets:
                # next set of the current exercise
                print('next set of the current exercise')
                self.current_set += 1
            else:
                # first set of the next exercise
                print('first set of the next exercise')
                self.current_pos += 1
                self.current_set = 1

        self.update_dialog()

    def weight_changed(self):
        # weight was changed --> update the ratio
        ratio = self.doubleSpinBox_weight.value() / self.baseline_weight
        self.doubleSpinBox_ratio.setValue(ratio)

    def ratio_changed(self):
        # ratio was changed --> update the weight
        weight = self.doubleSpinBox_ratio.value() * self.baseline_weight
        self.doubleSpinBox_weight.setValue(weight)

    def update_dialog(self):
        print('update dialog')
        self.update_labels()
        try:
            if self.current_pos in range(0, len(self.exercises)):
                self.set_values()
        except Exception as exc:
            print(exc)
            raise

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

        self.label_program.setText(f'{self.parent_tpr.training_theme.name}: {self.parent_tpr.name}')
        if self.current_pos <= -1:
            self.current_pos = -1
            self.baseline_weight = None
            self.baseline_duration = None

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
            score = self.assess_session()
            self.assess_session_set_text(score)

        elif self.current_pos >= len(self.exercises):
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
            score = self.assess_session()
            self.assess_session_set_text(score)
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
            self.label_sets.setText(f'Set {self.current_set} / {tex.baseline_sets}')

            if not self.baseline_weight:
                self.doubleSpinBox_weight.setEnabled(False)
                self.doubleSpinBox_ratio.setEnabled(False)
            if not self.baseline_duration:
                self.doubleSpinBox_duration.setEnabled(False)

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
            score = self.assess_exercise(tex, wex)
            self.assess_exercise_set_text(score)

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
            self.assess_exercise_set_text(None)

    @staticmethod
    def assess_exercise(tex: 'TrainingExercise', wex: Optional['WorkoutExercise']
                        ) -> Optional[float]:

        if wex:
            score = wex.repetitions / tex.baseline_repetitions
            if tex.baseline_weight:
                score *= wex.weight / tex.baseline_weight
            if tex.baseline_duration:
                score *= wex.duration / tex.baseline_duration
            return score

        return None  # if start / end or no wex yet

    def assess_exercise_set_text(self, score: Optional['float']):
        if score:
            self.lineEdit_assessment.setText(f'{score*100:.2f} %')
        else:
            self.lineEdit_assessment.setText('Noch nicht gespeichert')

    def assess_session(self):

        score = 1
        skipped = 0
        print(self.exercises)
        for tex, wexes in self.exercises:
            tex_score = 1
            wex_skipped = 0
            for i, wex in enumerate(wexes):
                if wex:
                    if i < tex.baseline_sets:
                        tex_score *= self.assess_exercise(tex, wex)
                    else:  # additional sets increase with +
                        tex_score += self.assess_exercise(tex, wex) / tex.baselin_sets

                else:  # no workout saved for the set
                    print('no workout saved for the set')
                    # print(tex_score, tex_score / tex.baseline_sets)
                    # tex_score -= tex_score / tex.baseline_sets
                    wex_skipped += 1
            tex_score -= tex_score * wex_skipped / len(wexes)
            if tex_score == 0:
                print('no exercise saved for tex', tex)
                skipped += 1
            else:
                score *= tex_score

        score -= score * skipped / len(self.exercises)

        return score

    def assess_session_set_text(self, score: Optional[float]):
        if not score:
            score = self.assess_session()

        if score == float(0):
            self.lineEdit_assessment.setText('Noch keine Übungen gespeichert.')
        else:
            self.lineEdit_assessment.setText(f'{score*100:.2f} %')

