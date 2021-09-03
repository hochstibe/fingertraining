# fingertraining
# Stefan Hochuli, 20.07.2021,
# Folder: speck_weg/ui File: dialog_training_exercise.py
#


from typing import TYPE_CHECKING, Optional

from PyQt5.QtWidgets import QDialog
import PyQt5.QtCore

from ..models import TrainingExerciseModel, TrainingProgramExerciseModel
from .dialog_training_exercise_ui import Ui_Dialog_training_exercise
from .dialog_training_exercise_load import ExerciseLoadDialog

if TYPE_CHECKING:
    from ..db import CRUD
    from ..models import TrainingProgramModel, UserModel


user_role = PyQt5.QtCore.Qt.UserRole


class ExerciseDialog(QDialog, Ui_Dialog_training_exercise):

    def __init__(self, db: 'CRUD', parent=None,
                 obj: 'TrainingExerciseModel' = None, parent_tpr: 'TrainingProgramModel' = None,
                 usr: 'UserModel' = None):
        super().__init__(parent)

        self.db = db

        self.tex: Optional['TrainingExerciseModel'] = obj
        self.parent_tpr: 'TrainingProgramModel' = parent_tpr
        self.usr: 'UserModel' = usr

        self.setupUi(self)
        self.connect()

        if self.tex:
            self.lineEdit_name.setText(self.tex.name)
            self.textEdit_description.setText(self.tex.description)
            self.spinBox_sets.setValue(self.tex.baseline_sets)
            self.spinBox_repetitions.setValue(self.tex.baseline_repetitions)

            if self.tex.baseline_weight:
                self.checkBox_weight.setChecked(True)
                self.checkBox_body_weight.setChecked(False)
                self.doubleSpinBox_weight.setValue(self.tex.baseline_weight)
            elif self.tex.tex_usr_id:
                self.checkBox_weight.setChecked(False)
                self.checkBox_body_weight.setChecked(True)
                self.doubleSpinBox_weight.setValue(self.usr.weight)
            else:
                self.checkBox_weight.setChecked(False)
                self.checkBox_body_weight.setChecked(False)
                self.doubleSpinBox_weight.setEnabled(False)
            if self.tex.baseline_duration:
                self.checkBox_duration.setChecked(True)
                self.doubleSpinBox_duration.setValue(self.tex.baseline_duration)
            else:
                self.checkBox_duration.setChecked(False)
                self.doubleSpinBox_duration.setEnabled(False)

    @property
    def max_sequence(self) -> int:
        if self.parent_tpr.training_exercises:
            return max([tpe.sequence for tpe in self.parent_tpr.training_exercises])
        else:
            return 0

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_import.clicked.connect(self.import_exercise)
        self.pushButton_save.clicked.connect(self.save)
        self.checkBox_weight.clicked.connect(self.weight_clicked)
        self.checkBox_body_weight.clicked.connect(self.body_weight_clicked)
        self.checkBox_duration.clicked.connect(self.duration_clicked)

    def import_exercise(self):
        print('import exercise')
        try:
            dialog = ExerciseLoadDialog(parent=self, db=self.db,
                                        parent_tpr=self.parent_tpr, usr=self.usr)
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                print('closing import dialog, nothing saved')
                self.clear_input()
        except Exception as exc:
            print(exc)
            raise

    def save(self):
        # Return the object, add to the db from main window
        if self.tex:
            print('editing')
            self.update_exercise_object()

            self.db.update()

        else:
            print('new tex')
            self.tex = TrainingExerciseModel()

            self.update_exercise_object()

            # Association with the sequence
            tpr_tex = TrainingProgramExerciseModel(sequence=self.max_sequence + 1)
            tpr_tex.training_exercise = self.tex
            tpr_tex.training_program = self.parent_tpr

            self.db.create(self.tex)
            print('tex added to the database')

            self.clear_input()

    def clear_input(self):
        # Clear after saving for adding a new one
        self.lineEdit_name.clear()
        self.textEdit_description.clear()

        # Reset the focus on the first lineEdit
        self.lineEdit_name.setFocus()
        self.tex = None

    def weight_clicked(self):

        if self.checkBox_weight.isChecked():
            # self.checkBox_body_weight.setEnabled(True)
            self.doubleSpinBox_weight.clear()  # clear body weight (if in spinbox)
            self.doubleSpinBox_weight.setEnabled(True)
            self.checkBox_body_weight.setChecked(False)
        else:
            self.doubleSpinBox_weight.clear()
            self.doubleSpinBox_weight.setEnabled(False)
            # self.checkBox_body_weight.(False)

    def body_weight_clicked(self):

        if self.checkBox_body_weight.isChecked():
            self.doubleSpinBox_weight.setValue(self.usr.weight)
            self.doubleSpinBox_weight.setEnabled(False)
            self.checkBox_weight.setChecked(False)
        else:
            self.doubleSpinBox_weight.clear()
            self.doubleSpinBox_weight.setEnabled(False)

    def duration_clicked(self, duration: float = None):
        if duration:
            self.doubleSpinBox_duration.setValue(duration)

        if self.checkBox_duration.isChecked():
            self.doubleSpinBox_duration.setEnabled(True)
        else:
            self.doubleSpinBox_duration.clear()
            self.doubleSpinBox_duration.setEnabled(False)

    def update_exercise_object(self):
        if self.tex:
            self.tex.name = self.lineEdit_name.text()
            self.tex.description = self.textEdit_description.toPlainText()
            self.tex.baseline_sets = self.spinBox_sets.value()
            self.tex.baseline_repetitions = self.spinBox_repetitions.value()
            if self.checkBox_weight.isChecked():
                print('custom weight')
                self.tex.baseline_weight = self.doubleSpinBox_weight.value()
            elif self.checkBox_body_weight.isChecked():
                print('body weight')
                self.tex.tex_usr_id = self.usr.usr_id
            else:
                print('no weight')
                self.tex.baseline_weight = None
                self.tex.tex_usr_id = None
            if self.checkBox_duration.isChecked():
                print('duration')
                self.tex.baseline_duration = self.doubleSpinBox_duration.value()
            else:
                print('no duration')
                self.tex.baseline_duration = None
        else:
            raise ValueError('No Training program object for updating.')
