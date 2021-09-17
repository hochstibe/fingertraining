# fingertraining
# Stefan Hochuli, 20.07.2021,
# Folder: speck_weg/ui File: dialog_training_exercise.py
#

from typing import TYPE_CHECKING, Dict

from PyQt5.QtWidgets import QDialog
import PyQt5.QtCore

from .dialog_training_exercise_ui import Ui_Dialog_training_exercise
from .dialog_training_exercise_load import ExerciseLoadDialog
from ..app import TrainingExercise

if TYPE_CHECKING:
    from ..db import CRUD


user_role = PyQt5.QtCore.Qt.UserRole


class ExerciseDialog(TrainingExercise, QDialog, Ui_Dialog_training_exercise):

    def __init__(self, db: 'CRUD', usr_id: int, tpr_id: int,
                 tex_id: int = None, parent=None):
        super().__init__(db=db, usr_id=usr_id, tpr_id=tpr_id,
                         tex_id=tex_id, parent=parent)

        self.setupUi(self)
        self.connect()

        self.update_widgets()

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

        dialog = ExerciseLoadDialog(parent=self, db=self.db, tpr_id=self.parent_model.tpr_id,
                                    usr_id=self.user_model.usr_id)
        dialog.exec()

        # rejected handles escape-key, x and the close button (connected to reject()
        if dialog.rejected:
            print('closing import dialog, nothing saved')
            # Clear the model in TrainingExercise -> free for creating a new one
            self.model = None  # not able to clear it from TrainingExerciseCollection
            self.read_objects()
            # Not sure, if this is necessary (depending on handling the sessions)
            # currently not necessary, because there is only one session for all actions
            self.update_widgets()  # clear model in in TrainingExercise.model

    def save(self):
        # Return the object, add to the db from main window
        if self.model:
            print('editing')
            kwargs = self.kwargs_from_widgets()
            self.edit_exercise(**kwargs)

        else:
            print('new tex')
            kwargs = self.kwargs_from_widgets()
            self.add_exercise(**kwargs)

            self.update_widgets()

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
            self.doubleSpinBox_weight.setValue(self.user_model.weight)
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

    def kwargs_from_widgets(self) -> Dict:

        kwargs = dict(name=self.lineEdit_name.text(),
                      description=self.textEdit_description.toPlainText(),
                      baseline_sets=self.spinBox_sets.value(),
                      baseline_repetitions=self.spinBox_repetitions.value())
        if self.checkBox_weight.isChecked():
            print('custom weight')
            baseline_weight = self.doubleSpinBox_weight.value()
            tex_usr_id = None
        elif self.checkBox_body_weight.isChecked():
            print('body weight')
            baseline_weight = None
            tex_usr_id = self.user_model.usr_id
        else:
            print('no weight')
            baseline_weight = None
            tex_usr_id = None
        if self.checkBox_duration.isChecked():
            print('duration')
            baseline_duration = self.doubleSpinBox_duration.value()
        else:
            print('no duration')
            baseline_duration = None
        kwargs['baseline_weight'] = baseline_weight
        kwargs['tex_usr_id'] = tex_usr_id
        kwargs['baseline_duration'] = baseline_duration

        return kwargs

    def update_widgets(self):
        # updates the widgets from the model
        print('updating widgets')
        if self.model:
            print('  from model')
            # editing -> get values from model
            self.lineEdit_name.setText(self.model.name)
            self.textEdit_description.setText(self.model.description)
            self.spinBox_sets.setValue(self.model.baseline_sets)
            self.spinBox_repetitions.setValue(self.model.baseline_repetitions)

            if self.model.baseline_custom_weight:
                self.checkBox_weight.setChecked(True)
                self.checkBox_body_weight.setChecked(False)
                self.doubleSpinBox_weight.setValue(self.model.baseline_custom_weight)
            elif self.model.tex_usr_id:
                self.checkBox_weight.setChecked(False)
                self.checkBox_body_weight.setChecked(True)
                self.doubleSpinBox_weight.setValue(self.user_model.weight)
            else:
                self.checkBox_weight.setChecked(False)
                self.checkBox_body_weight.setChecked(False)
                self.doubleSpinBox_weight.setEnabled(False)
            if self.model.baseline_duration:
                self.checkBox_duration.setChecked(True)
                self.doubleSpinBox_duration.setValue(self.model.baseline_duration)
            else:
                self.checkBox_duration.setChecked(False)
                self.doubleSpinBox_duration.setEnabled(False)
        else:
            print('  default values')
            self.lineEdit_name.clear()
            self.textEdit_description.clear()
            # leave the checkbox / spinbox
            # -> usually for the next exercise the same

            # Reset the focus on the first lineEdit
            self.lineEdit_name.setFocus()
