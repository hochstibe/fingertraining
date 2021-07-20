# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder:  File: main.py
#

import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QDialog
)
import PyQt5.QtCore
# from PyQt5.uic import loadUi  # --> import error? -> no direct loading -> create Classes with pyuic5 first
from sqlalchemy import select

from speck_weg.db import session
from speck_weg.models import TrainingProgram, TrainingPlan

from ui.main_window_ui import Ui_MainWindow_training
from ui.training_program_ui import Ui_dialog_training_program

user_role = PyQt5.QtCore.Qt.UserRole
# list items access data by their role (display role for text, user_role for data, ...)


class Window(QMainWindow, Ui_MainWindow_training):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.refresh_program_list()
        self.connect()

    def connect(self):
        """
        Connect all signals to their slots
        """
        self.action_about.triggered.connect(self.about)
        # Program
        self.listWidget_program.clicked.connect(self.program_list_clicked)
        self.pushButton_add_program.clicked.connect(self.new_program)
        self.pushButton_remove_program.clicked.connect(self.delete_program)
        # Plan
        self.listWidget_plan.clicked.connect(self.plan_list_clicked)

    def refresh_program_list(self):
        print('refreshing list')
        stmt = select(TrainingProgram)
        obj = session.execute(stmt).scalars()  # without scalars --> rows with lists of obj

        self.listWidget_program.clear()

        for i, tpr in enumerate(obj):
            print(i, tpr)
            self.listWidget_program.insertItem(i, tpr.tpr_name)
            self.listWidget_program.item(i).setData(user_role, tpr)

    def program_list_clicked(self):
        item = self.listWidget_program.currentItem()
        print('Clicked on the program list', item.text())

        self.refresh_plan_list(item.data(user_role))

    def new_program(self):
        dialog = ProgramDialog(self)
        dialog.pushButton_close.clicked.connect(self.refresh_program_list)

        dialog.exec()

    def delete_program(self):
        print('deleting')
        item = self.listWidget_program.currentItem()

        if item:
            session.delete(item.data(user_role))
            session.commit()
            print('item deleted')
        else:
            print('no item selected, none deleted')
        self.refresh_program_list()

    def refresh_plan_list(self, tpr: 'TrainingProgram'):
        print('refreshing plans')
        self.listWidget_plan.clear()

        for i, tpl in enumerate(tpr.training_plans):
            self.listWidget_plan.insertItem(i, tpl.tpl_name)
            self.listWidget_plan.item(i).setData(user_role, tpl)

    def plan_list_clicked(self):
        item = self.listWidget_plan.currentItem()
        print('Clicked on the plan list', item.text())

        self.refresh_exercise_list(item.data(user_role))

    def new_plan(self):
        pass

    def delete_plan(self):
        pass

    def refresh_exercise_list(self, tpl: 'TrainingPlan'):
        print('refreshing exercises')
        self.listWidget_plan.clear()

        for i, tpx in enumerate(tpl.training_exercises):
            self.listWidget_plan.insertItem(i, tpx.tpx_name)
            self.listWidget_plan.item(i).setData(user_role, tpx)

    @staticmethod
    def about():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Speck Weg!')
        msg.setText(f'Speck Weg! Version {0.1}')
        msg.setInformativeText('Stefan Hochuli, Copyright 2021')
        msg.setStandardButtons(QMessageBox.Close)

        msg.exec_()


class ProgramDialog(QDialog, Ui_dialog_training_program):

    tpr: 'TrainingProgram' = None

    def __init__(self, parent=None, obj: 'TrainingProgram' = None):
        super().__init__(parent)

        self.tpr = obj

        self.setupUi(self)
        self.connect()

        if self.tpr:
            self.set_edit_mode()
        else:
            self.set_new_mode()

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_save.clicked.connect(self.save)

    def save(self):
        # Return the object, add to the db from main window
        self.tpr = TrainingProgram(
            tpr_name=self.lineEdit_tpr_name.text(),
            tpr_description=self.lineEdit_tpr_description.text()
        )
        session.add(self.tpr)
        session.commit()
        print('tpr added to the database')

    def set_edit_mode(self):
        self.pushButton_save.setEnabled(False)
        self.pushButton_apply.setEnabled(True)

    def set_new_mode(self):
        self.pushButton_save.setEnabled(True)
        self.pushButton_apply.setEnabled(False)


if __name__ == "__main__":
    # Setup DB connection

    # Start ui
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
