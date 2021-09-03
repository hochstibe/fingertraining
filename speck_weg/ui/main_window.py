# fingertraining
# Stefan Hochuli, 20.07.2021,
# Folder: speck_weg/ui File: main_window.py
#

from typing import TYPE_CHECKING
import PyQt5.QtCore
from PyQt5.QtWidgets import QMainWindow

from . import ThemeDialog, ProgramDialog, ExerciseDialog, WorkoutDialog, UserDialog
from .messages import open_message_box
from .main_window_ui import Ui_MainWindow_training
from ..app import SpeckWeg

if TYPE_CHECKING:
    from ..db import CRUD

user_role = PyQt5.QtCore.Qt.UserRole


class MainWindow(SpeckWeg, QMainWindow, Ui_MainWindow_training):
    def __init__(self, db: 'CRUD', parent=None):
        super().__init__(db=db, parent=parent)

        # self.db = db

        self.setupUi(self)
        self.connect()

        # There must be one user in the database
        # self.usr = self.db.read_first(User)

        if not self.user.usr:
            print(self.user.usr)
            self.action_start_workout.setEnabled(False)

        self.theme_list_refresh()

    def connect(self):
        """
        Connect all signals to their slots
        """
        self.action_about.triggered.connect(self.about)
        # Theme
        self.listWidget_theme.clicked.connect(self.theme_list_clicked)
        self.listWidget_theme.model().rowsMoved.connect(self.theme_moved)
        self.pushButton_add_theme.clicked.connect(self.theme_new)
        self.pushButton_remove_theme.clicked.connect(self.theme_delete)
        self.pushButton_edit_theme.clicked.connect(self.theme_edit)
        # Program
        self.listWidget_program.clicked.connect(self.program_clicked)
        self.listWidget_program.model().rowsMoved.connect(self.program_moved)
        self.pushButton_add_program.clicked.connect(self.program_new)
        self.pushButton_remove_program.clicked.connect(self.program_delete)
        self.pushButton_edit_program.clicked.connect(self.program_edit)
        # Exercise
        # self.listWidget_exercise.clicked.connect(self.exercise_list_clicked)
        self.listWidget_exercise.model().rowsMoved.connect(self.exercise_moved)
        self.pushButton_add_exercise.clicked.connect(self.exercise_new)
        self.pushButton_remove_exercise.clicked.connect(self.exercise_delete)
        self.pushButton_edit_exercise.clicked.connect(self.exercise_edit)

        # Actions: User, Workout
        self.action_user_info.triggered.connect(self.edit_user)
        self.action_start_workout.triggered.connect(self.start_workout)

        # self.listWidget_program.itemSelectionChanged.connect(self.tester)

    def theme_list_refresh(self):
        print('refreshing list')
        # stmt = select(TrainingTheme).order_by(TrainingTheme.sequence).order_by(TrainingTheme.name)
        # themes = self.db.read_stmt(stmt)
        # themes = self.db.read_all(TrainingTheme)

        # themes = self.read_themes()
        # read from db and store them in a list
        super().theme_list_refresh()

        # clear all lists
        self.listWidget_theme.clear()
        self.listWidget_program.clear()
        self.listWidget_exercise.clear()

        for i, tth in enumerate(self.themes):
            print(i, tth)
            self.listWidget_theme.insertItem(i, tth.name)
            self.listWidget_theme.item(i).setData(user_role, tth)

    def theme_moved(self):
        print('theme moved')
        # themes = []
        # for i in range(self.listWidget_theme.count()):
        #     tth = self.listWidget_theme.item(i).data(user_role)
        #     themes.append(tth)
        #     # tth.sequence = i + 1
        # self.db.update()

        themes = [self.listWidget_theme.item(i).data(user_role)
                  for i in range(self.listWidget_theme.count())]

        self.update_themes_sequence(themes)

        self.program_list_refresh()

    def theme_list_clicked(self):
        theme = self.listWidget_theme.currentItem()
        print('Clicked on the program theme', theme.text())

        self.program_list_refresh()

    def theme_new(self):
        print('new theme')
        themes_row = self.listWidget_theme.currentRow()
        n_themes = self.listWidget_theme.count()

        dialog = ThemeDialog(parent=self, db=self.db, max_sequence=n_themes)
        dialog.exec()

        # rejected handles escape-key, x and the close button (connected to reject()
        if dialog.rejected:
            print('closing dialog')
            self.theme_list_refresh()

            # select a program
            n_themes_new = self.listWidget_theme.count()

            if n_themes_new > n_themes:
                # a new one was added, set to last row
                self.listWidget_theme.setCurrentRow(n_themes_new - 1)
            elif themes_row != -1:
                # no new one, a row was previously selected
                self.listWidget_theme.setCurrentRow(themes_row)
            else:
                # no new one, none was selected
                pass
            self.program_list_refresh()

    def theme_edit(self):
        print('edit theme')
        theme = self.listWidget_theme.currentItem()
        row = self.listWidget_theme.currentRow()

        if theme:
            dialog = ThemeDialog(parent=self, db=self.db, obj=theme.data(user_role))
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.theme_list_refresh()
                # select the one as before
                self.listWidget_theme.setCurrentRow(row)
                self.program_list_refresh()

    def theme_delete(self):
        print('deleting theme')
        theme = self.listWidget_theme.currentItem()
        theme_row = self.listWidget_theme.currentRow()

        if theme:
            self.db.delete(theme.data(user_role))
            print('item deleted')

            self.theme_list_refresh()

            # select a theme
            if theme_row < self.listWidget_theme.count():
                self.listWidget_theme.setCurrentRow(theme_row)
            else:
                self.listWidget_theme.setCurrentRow(theme_row - 1)
            self.program_list_refresh()

        else:
            print('no item selected, none deleted')

    def program_list_refresh(self):
        print('refreshing programs')
        self.listWidget_program.clear()
        self.listWidget_exercise.clear()

        # selected theme
        theme = self.listWidget_theme.currentItem()

        if theme:
            tth = theme.data(user_role)
            # read all programs from db related to the theme
            # programs = self.db.read(TrainingProgram, TrainingProgram.tpr_tth_id, tth.tth_id)

            for i, tpr in enumerate(tth.training_programs):
                self.listWidget_program.insertItem(i, tpr.name)
                self.listWidget_program.item(i).setData(user_role, tpr)

    def program_moved(self):
        print('rows moved')
        for i in range(self.listWidget_program.count()):
            tpr = self.listWidget_program.item(i).data(user_role)
            tpr.sequence = i + 1
        self.db.update()

        self.exercise_list_refresh()

    def program_clicked(self):
        program = self.listWidget_program.currentItem()
        print('Clicked on the program list', program.text())

        self.exercise_list_refresh()

    def program_new(self):
        theme = self.listWidget_theme.currentItem()
        program_row = self.listWidget_program.currentRow()
        n_programs = self.listWidget_program.count()

        if theme:
            dialog = ProgramDialog(parent=self, db=self.db, parent_tth=theme.data(user_role))
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.program_list_refresh()

                # select a program
                n_programs_new = self.listWidget_program.count()

                if n_programs_new > n_programs:
                    # a new one was added, set to last row
                    self.listWidget_program.setCurrentRow(n_programs_new - 1)
                elif program_row != -1:
                    # no new one, a row was previously selected
                    self.listWidget_program.setCurrentRow(program_row)
                else:
                    # no new one, none was selected
                    pass
                self.exercise_list_refresh()

    def program_edit(self):
        theme = self.listWidget_theme.currentItem()
        program = self.listWidget_program.currentItem()
        row = self.listWidget_theme.currentRow()

        if program:
            dialog = ProgramDialog(parent=self, db=self.db,
                                   obj=program.data(user_role), parent_tth=theme.data(user_role))
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.program_list_refresh()
                # select the one as before
                self.listWidget_program.setCurrentRow(row)
                self.exercise_list_refresh()

    def program_delete(self):
        print('deleting program')
        program = self.listWidget_program.currentItem()
        program_row = self.listWidget_program.currentRow()

        if program:
            self.db.delete(program.data(user_role))
            print('item deleted')
            self.program_list_refresh()

            if program_row < self.listWidget_program.count():
                self.listWidget_program.setCurrentRow(program_row)
            else:
                self.listWidget_program.setCurrentRow(program_row - 1)

            self.exercise_list_refresh()

        else:
            print('no item selected, none deleted')

    def exercise_list_refresh(self):
        print('refreshing exercises')
        self.listWidget_exercise.clear()

        # selected program
        program = self.listWidget_program.currentItem()

        if program:
            print('refresh exercises for the selected program', program.text())
            tpr = program.data(user_role)

            for i, tpe in enumerate(tpr.training_exercises):
                self.listWidget_exercise.insertItem(i, tpe.training_exercise.name)
                self.listWidget_exercise.item(i).setData(user_role, tpe.training_exercise)
            print('refresh done')

    def exercise_moved(self):
        print('exercise moved')

        program = self.listWidget_program.currentItem()
        if program:  # should always be true (no program selected, no exercise displayed)
            tpr = program.data(user_role)
            for i in range(self.listWidget_exercise.count()):
                tex = self.listWidget_exercise.item(i).data(user_role)
                # select the association object to the tex
                tpe = [
                    tpe for tpe in tpr.training_exercises if tpe.tpe_tex_id == tex.tex_id
                ][0]
                tpe.sequence = i + 1
            self.db.update()

    def exercise_new(self):
        print('new exercise')
        program = self.listWidget_program.currentItem()
        exercise_row = self.listWidget_exercise.currentRow()
        n_exercises = self.listWidget_exercise.count()

        if program:
            print('opening dialog')
            dialog = ExerciseDialog(parent=self, db=self.db, parent_tpr=program.data(user_role),
                                    usr=self.user.usr)
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.exercise_list_refresh()
                n_exercises_new = self.listWidget_exercise.count()

                # select an exercise
                if n_exercises_new > n_exercises:
                    # a new one was added, set to last row
                    self.listWidget_exercise.setCurrentRow(n_exercises_new - 1)
                elif exercise_row != -1:
                    # no new one, a row was previously selected
                    self.listWidget_exercise.setCurrentRow(exercise_row)
                else:
                    # no new one, none was selected
                    pass

    def exercise_edit(self):
        program = self.listWidget_program.currentItem()
        exercise = self.listWidget_exercise.currentItem()
        row = self.listWidget_exercise.currentRow()

        if exercise:
            print('exercise selected')
            dialog = ExerciseDialog(parent=self, db=self.db,
                                    obj=exercise.data(user_role),
                                    parent_tpr=program.data(user_role),
                                    usr=self.user.usr)
            print('starting dialog')
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.exercise_list_refresh()
                # select
                self.listWidget_exercise.setCurrentRow(row)

    def exercise_delete(self):
        print('deleting exercise')
        exercise = self.listWidget_exercise.currentItem()
        exercise_row = self.listWidget_exercise.currentRow()

        if exercise:
            self.db.delete(exercise.data(user_role))
            print('item deleted')
        else:
            print('no item selected, none deleted')

        self.exercise_list_refresh()
        # select
        if exercise_row < self.listWidget_exercise.count():
            self.listWidget_exercise.setCurrentRow(exercise_row)
        else:
            self.listWidget_exercise.setCurrentRow(exercise_row - 1)

    def edit_user(self):
        print('editing user data', self.user.usr)

        dialog = UserDialog(db=self.db, parent=self, obj=self.user.usr)
        dialog.exec()

        # There must be one user in the database -> read again
        self.user.read_current_user()

        if self.user.usr:
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
            open_message_box(self.messages['no_program_selected'])

    def about(self):
        open_message_box(self.messages['about'])
