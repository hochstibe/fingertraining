# fingertraining
# Stefan Hochuli, 31.08.2021,
# Folder: speck_weg/app File: app.py
#

from typing import List, Dict, Optional, TYPE_CHECKING

from . import (TrainingThemeCollection, TrainingProgramCollection,
               TrainingProgramExerciseCollection, User, Message,
               WorkoutSessionCollection)

if TYPE_CHECKING:
    from ..db import CRUD


class SpeckWeg:
    def __init__(self, db: 'CRUD', **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db

        # There must be one user in the database
        # self.usr = self.read_user()
        self.user = User(self.db)

        # instead of only storing the themes in the widgets, store them in lists
        self.themes = TrainingThemeCollection(self.db)
        self.current_tth_id: Optional[int] = None
        self.programs = TrainingProgramCollection(self.db)
        self.current_tpr_id: Optional[int] = None
        self.exercises = TrainingProgramExerciseCollection(self.db)
        self.current_tpe_id: Optional[int] = None  # training_program_exercise is unique
        self.workouts = WorkoutSessionCollection(self.db)
        self.current_wse_id: Optional[int] = None

        # default messages
        self.messages: Dict[str, 'Message'] = dict()

        title = 'Kein User vorhanden.'
        text = 'Bitte zuerst einen User erstellen.'
        self.messages['no_user'] = Message(title, text, 'information')

        title = 'Übung löschen'
        text = 'Willst du die Übung wirklich löschen?'
        self.messages['delete_exercise'] = Message(title, text, 'question',
                                                   button_accept_name='Löschen')

        title = 'Kein Programm ausgewählt'
        text = 'Bitte wählen Sie ein Programm aus, um ein Workout zu starten.'
        self.messages['no_program_selected'] = Message(title, text, 'information')

        title = 'Speck Weg!'
        text = f'Speck Weg! Version {0.1}'
        informative_text = 'Stefan Hochuli, Copyright 2021\n' \
                           'Icons von https://fontawesome.com/'
        self.messages['about'] = Message(title, text, 'information', informative_text)

    def theme_list_refresh(self, new: bool = False):
        # refreshes all lists (all depending on the theme)

        print('theme model list', self.themes.model_list)

        n_themes_old = len(self.themes.model_list)
        self.themes.read_themes()
        n_themes_new = len(self.themes.model_list)
        tth_ids = [tth.tth_id for tth in self.themes.model_list]
        print('refreshing themes, bevore active:', self.current_tth_id)

        if n_themes_new > n_themes_old and new:
            # a theme was added -> active is the newest / last one
            self.current_tth_id = self.themes.model_list[-1].tth_id
        elif self.current_tth_id:
            # one was previously selected
            if self.current_tth_id in tth_ids:
                # the id is still in the themes list
                pass
            else:
                # does not exist anymore
                self.current_tth_id = None
        else:
            # no new one, none was selected
            pass

        print('refreshing themes, now active:', self.current_tth_id)
        self.program_list_refresh()

    def update_themes_sequence(self, ids: List[int]):
        self.themes.update_sequence(ids)
        if self.current_tth_id not in ids:
            self.current_tth_id = None
        # reading the themes again is included in themes.update_sequence()

    def theme_delete(self):
        print('deleting', self.current_tth_id)
        tth_ids = [tth.tth_id for tth in self.themes.model_list]
        idx = tth_ids.index(self.current_tth_id)

        self.themes.remove_theme(tth_id=self.current_tth_id)
        # set another theme active
        if idx < len(self.themes.model_list):
            # was not the last one, select the previous position
            self.current_tth_id = self.themes.model_list[idx].tth_id
        elif len(self.themes.model_list) == 0:
            self.current_tth_id = None
        else:
            # was the last in the list -> set the current last one
            self.current_tth_id = self.themes.model_list[-1].tth_id

    def program_list_refresh(self, new: bool = False):
        # read from db, store in list
        # self.themes = self.themes_api.read_themes()
        if self.current_tth_id:
            # refresh the programs
            n_programs_old = len(self.programs.model_list)
            self.programs.read_programs(self.current_tth_id)
            n_programs_new = len(self.programs.model_list)
            tpr_ids = [tpr.tpr_id for tpr in self.programs.model_list]

            if n_programs_new > n_programs_old and new:
                # a program was added -> active is the newest / last one
                self.current_tpr_id = self.programs.model_list[-1].tpr_id
            elif self.current_tpr_id:
                # one was previously selected
                if self.current_tpr_id in tpr_ids:
                    # the id is still in the themes list
                    pass
                else:
                    # does not exist anymore
                    print('current_tpr_id does not exist anymore')
                    self.current_tpr_id = None
            else:
                # no new one, none was selected
                print('current_tpr_id no new one, none was selected')
                pass

        else:
            print('refreshing programs -> no tth_id given -> no programs')
            self.programs.model_list = []
            self.current_tpr_id = None

        self.exercise_list_refresh()

    def update_program_sequence(self, ids: List[int]):
        if self.current_tth_id:
            self.programs.update_sequence(ids, self.current_tth_id)
            if self.current_tpr_id not in ids:
                self.current_tpr_id = None
            # reading is included in programs.update_sequence()
        else:
            raise ValueError('updating program sequence not possible without self.current_tth_id')

    def program_delete(self):
        print('deleting', self.current_tpr_id)
        tpr_ids = [tpr.tpr_id for tpr in self.programs.model_list]
        idx = tpr_ids.index(self.current_tpr_id)

        self.programs.remove_program(tpr_id=self.current_tpr_id)
        # set another theme active
        if idx < len(self.programs.model_list):
            # was not the last one, select the previous position
            self.current_tpr_id = self.programs.model_list[idx].tpr_id
        elif len(self.programs.model_list) == 0:
            self.current_tpr_id = None
        else:
            # was the last in the list -> set the current last one
            self.current_tpr_id = self.programs.model_list[-1].tpr_id

    def exercise_list_refresh(self, new: bool = False):
        # read from db, store in list
        if self.current_tpr_id:
            # refresh the exercises
            n_exercises_old = len(self.exercises.model_list)
            self.exercises.read_exercises(self.current_tpr_id)
            n_exercises_new = len(self.exercises.model_list)
            tpe_ids = [tpe.tpe_id for tpe in self.exercises.model_list]
            print('refreshing exercises', tpe_ids, self.current_tpe_id)

            if n_exercises_new > n_exercises_old and new:
                # an exercise was added -> active is the newest / last one
                print('an exercise was added -> active is the newest / last one')
                self.current_tpe_id = self.exercises.model_list[-1].tpe_id
            elif self.current_tpe_id:
                # one was previously selected
                print('one was previously selected')
                if self.current_tpe_id in tpe_ids:
                    # the id is still in the themes list
                    print('the id is still in the themes list')
                    pass
                else:
                    # does not exist anymore
                    print('does not exist anymore')
                    self.current_tpe_id = None
            else:
                # no new one, none was selected
                pass

            print('refreshing exercises', tpe_ids, self.current_tpe_id)
        else:
            print('refreshing exercises -> no tpr_id given -> no exercises')
            self.exercises.model_list = []
            self.current_tpe_id = None

    def update_exercise_sequence(self, ids: List[int]):
        if self.current_tpr_id:
            self.exercises.update_sequence(ids, self.current_tpr_id)
            if self.current_tpe_id not in ids:
                self.current_tpe_id = None
            # reading is included in programs.update_sequence()
        else:
            raise ValueError('updating program sequence not possible without self.current_tth_id')

    def exercise_delete(self, child: bool = False):
        print('deleting', self.current_tpe_id)
        tpe_ids = [tpe.tpe_id for tpe in self.exercises.model_list]
        idx = tpe_ids.index(self.current_tpe_id)

        self.exercises.remove_exercise(tpe_id=self.current_tpe_id, child=child)
        # set another theme active
        if idx < len(self.exercises.model_list):
            # was not the last one, select the previous position
            self.current_tpe_id = self.exercises.model_list[idx].tpe_id
        elif len(self.exercises.model_list) == 0:
            self.current_tpe_id = None
        else:
            # was the last in the list -> set the current last one
            self.current_tpe_id = self.exercises.model_list[-1].tpe_id

    def workout_list_refresh(self, new: bool = False):
        # read from db, store in list
        # self.themes = self.themes_api.read_themes()

        # if self.current_tpr_id:
        # refresh the programs -> all sessions if no program selected
        n_workouts_old = len(self.workouts.workout_list)

        self.workouts.read_sessions(self.current_tpr_id, self.current_tth_id)
        n_workouts_new = len(self.workouts.workout_list)
        wse_ids = [workout.model.wse_id for workout in self.workouts.workout_list]

        if n_workouts_new > n_workouts_old and new:
            # a program was added -> active is the newest / last one
            self.current_wse_id = self.workouts.workout_list[-1].model.wse_id
        elif self.current_wse_id:
            # one was previously selected
            if self.current_wse_id in wse_ids:
                # the id is still in the themes list
                pass
            else:
                # does not exist anymore
                print('current_tpr_id does not exist anymore')
                self.current_wse_id = None
        else:
            # no new one, none was selected
            print('current_tpr_id no new one, none was selected')
            pass
