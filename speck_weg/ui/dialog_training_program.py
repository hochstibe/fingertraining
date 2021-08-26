# fingertraining
# Stefan Hochuli, 20.07.2021,
# Folder: speck_weg/ui File: dialog_training_program.py
#


from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QDialog
import PyQt5.QtCore

from ..models import TrainingProgram
from .dialog_training_program_ui import Ui_Dialog_training_program

if TYPE_CHECKING:
    from ..db import CRUD
    from ..models import TrainingTheme


user_role = PyQt5.QtCore.Qt.UserRole


class ProgramDialog(QDialog, Ui_Dialog_training_program):

    tpr: 'TrainingProgram' = None

    def __init__(self, db: 'CRUD', parent=None,
                 obj: 'TrainingProgram' = None, parent_tth: 'TrainingTheme' = None):
        super().__init__(parent)

        self.db = db

        self.tpr = obj
        self.parent_tth = parent_tth

        self.setupUi(self)
        self.connect()

        # if self.tpr:
        #     self.set_edit_mode()
        # else:
        #     self.set_new_mode()

        if self.tpr:
            self.lineEdit_name.setText(self.tpr.name)
            self.lineEdit_description.setText(self.tpr.description)
        self.refresh_exercise_list()

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_up.clicked.connect(self.one_up)
        self.pushButton_down.clicked.connect(self.one_down)

    def save(self):
        # Return the object, add to the db from main window
        if self.tpr:
            print('editing')
            self.update_object()

            self.db.update()

            print('after update')
            for tex in self.tpr.training_exercises:
                print(tex, tex.sequence)
        else:
            print('new program')
            self.tpr = TrainingProgram(
                tpr_tth_id=self.parent_tth.tth_id,
            )
            #     name=self.lineEdit_name.text(),
            #     description=self.lineEdit_description.text()
            # )
            self.update_object()
            self.db.create(self.tpr)
            print('tpr added to the database')

            # Clear after saving for adding a new one
            self.lineEdit_name.clear()
            self.lineEdit_description.clear()
            # Reset the focus on the first lineEdit
            self.lineEdit_name.setFocus()

    def refresh_exercise_list(self):
        for i, tex in enumerate(self.tpr.training_exercises):
            self.listWidget_exercise.insertItem(i, tex.name)
            self.listWidget_exercise.item(i).setData(user_role, tex)

    def one_up(self):
        row = self.listWidget_exercise.currentRow()
        item = self.listWidget_exercise.takeItem(row)
        self.listWidget_exercise.insertItem(row - 1, item)
        self.listWidget_exercise.setCurrentRow(row - 1)

    def one_down(self):
        row = self.listWidget_exercise.currentRow()
        item = self.listWidget_exercise.takeItem(row)
        self.listWidget_exercise.insertItem(row + 1, item)
        self.listWidget_exercise.setCurrentRow(row + 1)

    def update_object(self):
        if self.tpr:
            self.tpr.name = self.lineEdit_name.text()
            self.tpr.description = self.lineEdit_description.text()

            for i in range(self.listWidget_exercise.count()):
                tex = self.listWidget_exercise.item(i).data(user_role)
                tex.sequence = i + 1

        else:
            raise ValueError('No Training program object for updating.')

    # def set_edit_mode(self):
    #     self.pushButton_save.setEnabled(False)
    #     self.pushButton_apply.setEnabled(True)
    #     self.pushButton_apply.setDefault(True)

    # def set_new_mode(self):
    #     self.pushButton_apply.setEnabled(False)
    #     self.pushButton_save.setEnabled(True)
    #     self.pushButton_save.setDefault(True)
