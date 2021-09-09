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

        # self.showMaximized()

        # There must be one user in the database
        if not self.user.model:
            print(self.user.model)
            self.action_start_workout.setEnabled(False)

        self.theme_list_widget_refresh()

    def connect(self):
        """
        Connect all signals to their slots
        """
        self.action_about.triggered.connect(self.about_clicked)
        # Theme
        self.listWidget_theme.clicked.connect(self.theme_list_clicked)
        self.listWidget_theme.model().rowsMoved.connect(self.theme_moved)
        self.pushButton_add_theme.clicked.connect(self.theme_new_clicked)
        self.pushButton_remove_theme.clicked.connect(self.theme_delete_clicked)
        self.pushButton_edit_theme.clicked.connect(self.theme_edit_clicked)
        # Program
        self.listWidget_program.clicked.connect(self.program_clicked)
        self.listWidget_program.model().rowsMoved.connect(self.program_moved)
        self.pushButton_add_program.clicked.connect(self.program_new_clicked)
        self.pushButton_remove_program.clicked.connect(self.program_delete_clicked)
        self.pushButton_edit_program.clicked.connect(self.program_edit_clicked)
        # Exercise
        self.listWidget_exercise.clicked.connect(self.exercise_clicked)
        self.listWidget_exercise.model().rowsMoved.connect(self.exercise_moved)
        self.pushButton_add_exercise.clicked.connect(self.exercise_new_clicked)
        self.pushButton_remove_exercise.clicked.connect(self.exercise_delete_clicked)
        self.pushButton_edit_exercise.clicked.connect(self.exercise_edit_clicked)

        # Actions: User, Workout
        self.action_user_info.triggered.connect(self.edit_user_clicked)
        self.action_start_workout.triggered.connect(self.start_workout_clicked)

    def selection2attr(self):
        theme = self.listWidget_theme.currentItem()
        if theme:
            tth_id = theme.data(user_role)
            if tth_id in [m.tth_id for m in self.themes.model_list]:
                self.current_tth_id = theme.data(user_role)
            else:
                raise ValueError('Theme list needs to be refreshed before storing the current tth')
        else:
            self.current_tth_id = None
        program = self.listWidget_program.currentItem()
        if program:
            self.current_tpr_id = program.data(user_role)
        else:
            self.current_tpr_id = None
        exercise = self.listWidget_exercise.currentItem()
        if exercise:
            self.current_tpe_id = exercise.data(user_role)
        else:
            self.current_tpe_id = None

    def theme_list_widget_refresh(self, new: bool = False):
        print('refreshing list')
        # store selected id
        # self.selection2attr()
        # refresh from the database
        self.theme_list_refresh(new)

        # clear all lists
        self.listWidget_theme.clear()
        self.listWidget_program.clear()
        self.listWidget_exercise.clear()

        # insert themes and select the previous one
        current_row = None
        for i, tth in enumerate(self.themes.model_list):
            print(i, tth)
            # ListWidget: Name and id
            self.listWidget_theme.insertItem(i, tth.name)
            self.listWidget_theme.item(i).setData(user_role, tth.tth_id)
            if tth.tth_id == self.current_tth_id:
                current_row = i
        # set the current row
        if isinstance(current_row, int):
            self.listWidget_theme.setCurrentRow(current_row)

        # refreshes the program list (based on the current_tth_id)
        self.program_list_widget_refresh()

    def theme_moved(self):
        print('theme moved')
        # themes = []
        # for i in range(self.listWidget_theme.count()):
        #     tth = self.listWidget_theme.item(i).data(user_role)
        #     themes.append(tth)
        #     # tth.sequence = i + 1
        # self.db.update()

        # list of ids for the new ordering sequence
        tth_ids = [self.listWidget_theme.item(i).data(user_role)
                   for i in range(self.listWidget_theme.count())]

        # update the selection
        self.selection2attr()
        # store the sequence
        self.update_themes_sequence(tth_ids)

        # refresh the list not necessary (should now be in the same order as self.themes.models

        self.program_list_widget_refresh()

    def theme_list_clicked(self):
        theme = self.listWidget_theme.currentItem()
        print('Clicked on the program theme', theme.text())

        # update the selection
        self.selection2attr()
        # refresh programs
        self.program_list_widget_refresh()

    def theme_new_clicked(self):
        print('new theme')
        n_themes = self.listWidget_theme.count()  # or len(self.themes.model_list

        dialog = ThemeDialog(parent=self, db=self.db, max_sequence=n_themes)
        dialog.exec()

        # rejected handles escape-key, x and the close button (connected to reject()
        if dialog.rejected:
            print('closing dialog')
            self.theme_list_widget_refresh(new=True)

    def theme_edit_clicked(self):
        print('edit theme')
        theme = self.listWidget_theme.currentItem()
        # row = self.listWidget_theme.currentRow()

        if theme:
            dialog = ThemeDialog(parent=self, db=self.db, tth_id=theme.data(user_role))
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.theme_list_widget_refresh()

    def theme_delete_clicked(self):
        print('deleting theme')
        theme = self.listWidget_theme.currentItem()
        theme_row = self.listWidget_theme.currentRow()

        if theme:
            # self.db.delete(theme.data(user_role))
            self.theme_delete()
            print('item deleted in db')
            self.listWidget_theme.takeItem(theme_row)

            tth_ids = [self.listWidget_theme.item(i).data(user_role)
                       for i in range(self.listWidget_theme.count())]
            for i, tth_id in enumerate(tth_ids):
                if tth_id == self.current_tth_id:
                    self.listWidget_theme.setCurrentRow(i)
            # print('item removed from gui')
            # no refreshing -> refresh_list is overloaded with gui2app

            # select a theme
            # if theme_row < self.listWidget_theme.count():
            #     self.listWidget_theme.setCurrentRow(theme_row)
            # else:
            #     self.listWidget_theme.setCurrentRow(theme_row - 1)
            self.program_list_widget_refresh()

        else:
            print('no item selected, none deleted')

    def program_list_widget_refresh(self, new: bool = False):
        print('refreshing programs')
        self.listWidget_program.clear()
        self.listWidget_exercise.clear()

        # selected theme
        # maybe delete, if working more with self.current_tth? maybe safer with listWidget?
        theme = self.listWidget_theme.currentItem()

        if theme:
            self.program_list_refresh(new)

            # insert from the model list
            current_row = None
            for i, tpr in enumerate(self.programs.model_list):
                print(i, tpr)
                # ListWidget: Name and
                self.listWidget_program.insertItem(i, tpr.name)
                self.listWidget_program.item(i).setData(user_role, tpr.tpr_id)
                if tpr.tpr_id == self.current_tpr_id:
                    current_row = i
            # set the current row
            if isinstance(current_row, int):
                self.listWidget_program.setCurrentRow(current_row)
        else:
            # only for safety, should already be None from super().
            self.current_tpr_id = None
        print('programs updated')

        self.exercise_list_widget_refresh()

    def program_moved(self):
        print('rows moved')

        # list of ids for the new ordering sequence
        tpr_ids = [self.listWidget_program.item(i).data(user_role)
                   for i in range(self.listWidget_program.count())]

        # update the selection
        self.selection2attr()
        # store the sequence
        self.update_program_sequence(tpr_ids)

        # refresh the list not necessary (should now be in the same order as self.themes.models

        self.exercise_list_widget_refresh()

    def program_clicked(self):
        program = self.listWidget_program.currentItem()
        print('Clicked on the program list', program.text())

        # update the selection
        self.selection2attr()

        # refresh the exercises
        self.exercise_list_widget_refresh()

    def program_new_clicked(self):
        theme = self.listWidget_theme.currentItem()
        n_programs = self.listWidget_program.count()  # or len(self.programs.model_list)

        if theme:
            dialog = ProgramDialog(parent=self, db=self.db, tpr_tth_id=theme.data(user_role),
                                   max_sequence=n_programs)
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.program_list_widget_refresh(new=True)

    def program_edit_clicked(self):
        theme = self.listWidget_theme.currentItem()
        program = self.listWidget_program.currentItem()

        if program and theme:
            dialog = ProgramDialog(parent=self, db=self.db, tpr_tth_id=theme.data(user_role),
                                   tpr_id=program.data(user_role))
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.program_list_widget_refresh()

    def program_delete_clicked(self):
        print('deleting program')
        program = self.listWidget_program.currentItem()
        program_row = self.listWidget_program.currentRow()

        if program:
            self.program_delete()
            print('item deleted')
            self.listWidget_program.takeItem(program_row)

            tpr_ids = [self.listWidget_program.item(i).data(user_role)
                       for i in range(self.listWidget_program.count())]
            for i, tpr_id in enumerate(tpr_ids):
                if tpr_id == self.current_tpr_id:
                    self.listWidget_program.setCurrentRow(i)

            self.exercise_list_widget_refresh()

        else:
            print('no item selected, none deleted')

    def exercise_list_widget_refresh(self, new: bool = False):
        print('refreshing exercises')
        self.listWidget_exercise.clear()

        # selected program
        program = self.listWidget_program.currentItem()

        if program:
            print('refresh exercises for the selected program', program.text())
            self.exercise_list_refresh(new)

            # insert from the model list
            current_row = None
            for i, tpe in enumerate(self.exercises.model_list):
                print(i, tpe)
                self.listWidget_exercise.insertItem(i, tpe.training_exercise.name)
                self.listWidget_exercise.item(i).setData(user_role, tpe.tpe_id)
                print(self.current_tpe_id, tpe.tpe_id)
                if tpe.tpe_id == self.current_tpe_id:
                    current_row = i
                    print('current row', current_row)
            # set the current row
            if isinstance(current_row, int):
                self.listWidget_exercise.setCurrentRow(current_row)
        else:
            # only for safety, should already be None from super().
            self.current_tpr_id = None
            print('refresh done')

    def exercise_moved(self):
        print('exercise moved')

        # list of ids for the new ordering sequence
        tpe_ids = [self.listWidget_exercise.item(i).data(user_role)
                   for i in range(self.listWidget_exercise.count())]

        # update the selection
        self.selection2attr()
        # store the sequence
        self.update_exercise_sequence(tpe_ids)

        # refresh the list not necessary (should now be in the same order as self.themes.models

    def exercise_clicked(self):
        # update the selection
        self.selection2attr()

    def exercise_new_clicked(self):
        print('new exercise')
        program = self.listWidget_program.currentItem()
        n_exercises = self.listWidget_exercise.count()

        if program:
            print('opening dialog')
            dialog = ExerciseDialog(parent=self, db=self.db, usr_id=self.user.model.usr_id,
                                    tpr_id=program.data(user_role), max_sequence=n_exercises)
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.exercise_list_widget_refresh(new=True)

    def exercise_edit_clicked(self):
        program = self.listWidget_program.currentItem()
        exercise = self.listWidget_exercise.currentItem()

        if exercise and program:
            print('exercise selected')
            # get the tex_id from the tpe model
            tpe_id = exercise.data(user_role)
            tpe = next(tpe for tpe in self.exercises.model_list if tpe.tpe_id == tpe_id)
            dialog = ExerciseDialog(parent=self, db=self.db, usr_id=self.user.model.usr_id,
                                    tpr_id=program.data(user_role),
                                    tex_id=tpe.training_exercise.tex_id)
            print('starting dialog')
            dialog.exec()

            # rejected handles escape-key, x and the close button (connected to reject()
            if dialog.rejected:
                self.exercise_list_widget_refresh()

    def exercise_delete_clicked(self):
        print('deleting exercise')
        exercise = self.listWidget_exercise.currentItem()
        exercise_row = self.listWidget_exercise.currentRow()

        if exercise:
            tex = next(tpe.training_exercise
                       for tpe in self.exercises.model_list
                       if tpe.tpe_id == self.current_tpe_id)
            last_exercise = self.exercises.check_for_last_exercise(tex.tex_id)
            print(tex, last_exercise)
            delete = True
            if last_exercise:
                message = self.messages['delete_exercise']
                clicked = open_message_box(message)
                if not clicked:
                    delete = False

            if delete:
                self.exercise_delete()
                print('item deleted')
                self.listWidget_exercise.takeItem(exercise_row)

                tpe_ids = [self.listWidget_exercise.item(i).data(user_role)
                           for i in range(self.listWidget_exercise.count())]
                for i, tpe_id in enumerate(tpe_ids):
                    if tpe_id == self.current_tpe_id:
                        self.listWidget_program.setCurrentRow(i)

        else:
            print('no item selected, none deleted')

    def edit_user_clicked(self):
        print('editing user data', self.user.model)

        dialog = UserDialog(db=self.db, parent=self, usr_id=self.user.model.usr_id)
        dialog.exec()

        if dialog.rejected:
            # There must be one user in the database -> read again
            self.user.read_current_user()

            if self.user.model:
                self.action_start_workout.setEnabled(True)
            else:
                self.action_start_workout.setEnabled(False)

    def start_workout_clicked(self):
        print('starting the workout dialog')

        program = self.listWidget_program.currentItem()

        if program:
            dialog = WorkoutDialog(db=self.db, parent=self, parent_tpr=program.data(user_role))

            dialog.exec()

        else:
            open_message_box(self.messages['no_program_selected'])

    def about_clicked(self):
        open_message_box(self.messages['about'])
