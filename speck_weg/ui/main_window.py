# fingertraining
# Stefan Hochuli, 20.07.2021, 
# Folder: speck_weg/ui File: main_window.py
#

from typing import TYPE_CHECKING
import PyQt5.QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from .dialogs import ProgramDialog, PlanDialog, ExerciseDialog
from ..models import TrainingProgram, TrainingPlan, TrainingExercise
from .main_window_ui import Ui_MainWindow_training

if TYPE_CHECKING:
    from ..db import CRUD

user_role = PyQt5.QtCore.Qt.UserRole


class Window(QMainWindow, Ui_MainWindow_training):
    def __init__(self, db: 'CRUD', parent=None):
        super().__init__(parent)

        self.db = db

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
        self.pushButton_add_plan.clicked.connect(self.new_plan)
        self.pushButton_remove_plan.clicked.connect(self.delete_plan)
        # Exercise
        self.listWidget_exercise.clicked.connect(self.exercise_list_clicked)
        self.pushButton_add_exercise.clicked.connect(self.new_exercise)
        self.pushButton_remove_exercise.clicked.connect(self.delete_exercise)

    def refresh_program_list(self):
        print('refreshing list')
        programs = self.db.read_all(TrainingProgram)

        self.listWidget_program.clear()

        for i, tpr in enumerate(programs):
            print(i, tpr)
            self.listWidget_program.insertItem(i, tpr.tpr_name)
            self.listWidget_program.item(i).setData(user_role, tpr)

    def program_list_clicked(self):
        item = self.listWidget_program.currentItem()
        print('Clicked on the program list', item.text())

        self.refresh_plan_list()

    def new_program(self):
        dialog = ProgramDialog(parent=self, db=self.db)
        dialog.pushButton_close.clicked.connect(self.refresh_program_list)

        dialog.exec()

    def delete_program(self):
        print('deleting')
        item = self.listWidget_program.currentItem()

        if item:
            self.db.delete(item.data(user_role))
            print('item deleted')
        else:
            print('no item selected, none deleted')
        self.refresh_program_list()

    def refresh_plan_list(self):
        print('refreshing plans')
        self.listWidget_plan.clear()

        # selected program
        program = self.listWidget_program.currentItem()

        # Todo: maybe simpler: use the tpr object in the listWidget

        if program:
            tpr = program.data(user_role)
            # read all plans from db related to the program
            plans = self.db.read(TrainingPlan, TrainingPlan.tpl_tpr_id, tpr.tpr_id)

            for i, tpl in enumerate(plans):
                self.listWidget_plan.insertItem(i, tpl.tpl_name)
                self.listWidget_plan.item(i).setData(user_role, tpl)

    def plan_list_clicked(self):
        item = self.listWidget_plan.currentItem()
        print('Clicked on the plan list', item.text())

        self.refresh_exercise_list()

    def new_plan(self):
        program = self.listWidget_program.currentItem()

        if program:
            dialog = PlanDialog(parent=self, db=self.db, parent_tpr=program.data(user_role))
            dialog.pushButton_close.clicked.connect(self.refresh_plan_list)

            dialog.exec()

    def delete_plan(self):
        print('deleting')
        plan = self.listWidget_plan.currentItem()

        if plan:
            self.db.delete(plan.data(user_role))
            print('item deleted')
        else:
            print('no item selected, none deleted')

        # update the list, if a program is selected
        # program = self.listWidget_program.currentItem()
        # if program:
        self.refresh_plan_list()

    def refresh_exercise_list(self):
        print('refreshing exercises')
        self.listWidget_exercise.clear()

        # selected plan
        plan = self.listWidget_plan.currentItem()

        # Todo: maybe simpler: use the tpr object in the listWidget

        if plan:
            tpl = plan.data(user_role)
            # read all plans from db related to the program
            exercises = self.db.read(TrainingExercise, TrainingExercise.tex_tpl_id, tpl.tpl_id)

            for i, tex in enumerate(exercises):
                self.listWidget_exercise.insertItem(i, tex.tex_name)
                self.listWidget_exercise.item(i).setData(user_role, tex)

    def exercise_list_clicked(self):
        item = self.listWidget_exercise.currentItem()
        print('Clicked on the exercise', item.text())

    def new_exercise(self):
        plan = self.listWidget_plan.currentItem()

        if plan:
            dialog = ExerciseDialog(parent=self, db=self.db, parent_tpl=plan.data(user_role))
            dialog.pushButton_close.clicked.connect(self.refresh_plan_list)

            dialog.exec()

    def delete_exercise(self):
        print('deleting')
        exercise = self.listWidget_exercise.currentItem()

        if exercise:
            self.db.delete(exercise.data(user_role))
            print('item deleted')
        else:
            print('no item selected, none deleted')

        # update the list, if a program is selected
        # program = self.listWidget_program.currentItem()
        # if program:
        self.refresh_exercise_list()

    @staticmethod
    def about():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Speck Weg!')
        msg.setText(f'Speck Weg! Version {0.1}')
        msg.setInformativeText('Stefan Hochuli, Copyright 2021')
        msg.setStandardButtons(QMessageBox.Close)

        msg.exec_()