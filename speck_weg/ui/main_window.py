# fingertraining
# Stefan Hochuli, 20.07.2021,
# Folder: speck_weg/ui File: main_window.py
#

from typing import TYPE_CHECKING
import PyQt5.QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from sqlalchemy import select, func

from . import ThemeDialog, ProgramDialog, ExerciseDialog, WorkoutDialog, UserDialog
from .main_window_ui import Ui_MainWindow_training
from ..models import TrainingTheme, TrainingProgram, TrainingExercise, User
from ..tables import tpr_tex_table

if TYPE_CHECKING:
    from ..db import CRUD

user_role = PyQt5.QtCore.Qt.UserRole


class MainWindow(QMainWindow, Ui_MainWindow_training):
    def __init__(self, db: 'CRUD', parent=None):
        super().__init__(parent)

        self.db = db

        self.setupUi(self)
        self.refresh_theme_list()
        self.connect()

        # There must be one user in the database
        self.usr = self.db.read_first(User)

        if not self.usr:
            self.action_start_workout.setEnabled(False)

    def connect(self):
        """
        Connect all signals to their slots
        """
        self.action_about.triggered.connect(self.about)
        # Program
        self.listWidget_theme.clicked.connect(self.theme_list_clicked)
        self.pushButton_add_theme.clicked.connect(self.new_theme)
        self.pushButton_remove_theme.clicked.connect(self.delete_theme)
        # Plan
        self.listWidget_program.clicked.connect(self.program_list_clicked)
        self.pushButton_add_program.clicked.connect(self.new_program)
        self.pushButton_remove_program.clicked.connect(self.delete_program)
        self.pushButton_edit_program.clicked.connect(self.edit_program)
        # Exercise
        self.listWidget_exercise.clicked.connect(self.exercise_list_clicked)
        self.pushButton_add_exercise.clicked.connect(self.new_exercise)
        self.pushButton_remove_exercise.clicked.connect(self.delete_exercise)

        # Actions: User, Workout
        self.action_user_info.triggered.connect(self.edit_user)
        self.action_start_workout.triggered.connect(self.start_workout)

    def refresh_theme_list(self):
        print('refreshing list')
        themes = self.db.read_all(TrainingTheme)

        self.listWidget_theme.clear()
        self.listWidget_program.clear()
        self.listWidget_exercise.clear()

        for i, tpr in enumerate(themes):
            print(i, tpr)
            self.listWidget_theme.insertItem(i, tpr.name)
            self.listWidget_theme.item(i).setData(user_role, tpr)

    def theme_list_clicked(self):
        theme = self.listWidget_theme.currentItem()
        print('Clicked on the program theme', theme.text())

        self.refresh_program_list()

    def new_theme(self):
        print('new theme')
        dialog = ThemeDialog(parent=self, db=self.db)
        dialog.exec()

        # rejected handles escape-key, x and the close button (connected to reject()
        if dialog.rejected:
            print('closing dialog')
            self.refresh_theme_list()

    def delete_theme(self):
        print('deleting theme')
        theme = self.listWidget_theme.currentItem()

        if theme:
            self.db.delete(theme.data(user_role))
            print('item deleted')
        else:
            print('no item selected, none deleted')
        self.refresh_theme_list()

    def refresh_program_list(self):
        print('refreshing programs')
        self.listWidget_program.clear()
        self.listWidget_exercise.clear()

        # selected theme
        theme = self.listWidget_theme.currentItem()

        # Todo: maybe simpler: use the tpr object in the listWidget

        if theme:
            tth = theme.data(user_role)
            # read all programs from db related to the theme
            # programs = self.db.read(TrainingProgram, TrainingProgram.tpr_tth_id, tth.tth_id)

            for i, tpr in enumerate(tth.training_programs):
                self.listWidget_program.insertItem(i, tpr.name)
                self.listWidget_program.item(i).setData(user_role, tpr)

    def program_list_clicked(self):
        program = self.listWidget_program.currentItem()
        print('Clicked on the program list', program.text())

        self.refresh_exercise_list()

    def new_program(self):
        theme = self.listWidget_theme.currentItem()

        if theme:
            dialog = ProgramDialog(parent=self, db=self.db, parent_tth=theme.data(user_role))
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.refresh_program_list()

    def edit_program(self):
        theme = self.listWidget_theme.currentItem()
        program = self.listWidget_program.currentItem()

        if program:
            dialog = ProgramDialog(parent=self, db=self.db,
                                   obj=program.data(user_role), parent_tth=theme.data(user_role))
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.refresh_program_list()

    def delete_program(self):
        print('deleting program')
        program = self.listWidget_program.currentItem()

        if program:
            self.db.delete(program.data(user_role))
            print('item deleted')
        else:
            print('no item selected, none deleted')

        # update the list, if a program is selected
        # program = self.listWidget_theme.currentItem()
        # if program:
        self.refresh_program_list()

    def refresh_exercise_list(self):
        print('refreshing exercises')
        self.listWidget_exercise.clear()

        # selected plan
        program = self.listWidget_program.currentItem()

        # Todo: maybe simpler: use the tpr object in the listWidget

        if program:
            print('refresh exercises for the selected program', program.text())
            tpr = program.data(user_role)

            for i, tex in enumerate(tpr.training_exercises):
                self.listWidget_exercise.insertItem(i, tex.name)
                self.listWidget_exercise.item(i).setData(user_role, tex)
        print('refresh done')

    def exercise_list_clicked(self):
        item = self.listWidget_exercise.currentItem()
        print('Clicked on the exercise', item.text())

    def new_exercise(self):
        print('new exercise')
        program = self.listWidget_program.currentItem()

        if program:
            print('opening dialog')
            dialog = ExerciseDialog(parent=self, db=self.db, parent_tpr=program.data(user_role),
                                    usr=self.usr)
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.refresh_exercise_list()

    def edit_exercise(self):
        program = self.listWidget_program.currentItem()
        exercise = self.listWidget_exercise.currentItem()

        if exercise:
            dialog = ExerciseDialog(parent=self, db=self.db,
                                    obj=exercise.data(user_role),
                                    parent_tpr=program.data(user_role),
                                    usr=self.usr)
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.refresh_program_list()

    def delete_exercise(self):
        print('deleting exercise')
        exercise = self.listWidget_exercise.currentItem()

        if exercise:
            self.db.delete(exercise.data(user_role))
            print('item deleted')
        else:
            print('no item selected, none deleted')

        # update the list, if a program is selected
        # program = self.listWidget_theme.currentItem()
        # if program:
        self.refresh_exercise_list()

    def edit_user(self):
        print('editing user data', self.usr)

        dialog = UserDialog(db=self.db, parent=self, obj=self.usr)
        dialog.exec()

        # There must be one user in the database
        self.usr = self.db.read_first(User)

        if self.usr:
            self.action_start_workout.setEnabled(True)
        else:
            self.action_start_workout.setEnabled(False)

    def start_workout(self):
        print('starting the workout dialog')

        program = self.listWidget_program.currentItem()

        if program:
            dialog = WorkoutDialog(db=self.db, parent=self, parent_tpr=program.data(user_role))

            dialog.exec()

        else:
            print('No program selected')
            msg = QMessageBox()

            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('Kein Programm ausgewählt')
            msg.setText('Bitte wählen Sie ein Programm aus, um ein Workout zu starten.')
            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec()

    @staticmethod
    def about():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Speck Weg!')
        msg.setText(f'Speck Weg! Version {0.1}')
        msg.setInformativeText('Stefan Hochuli, Copyright 2021')
        msg.setStandardButtons(QMessageBox.Close)

        msg.exec()
