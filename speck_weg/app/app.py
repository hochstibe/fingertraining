# fingertraining
# Stefan Hochuli, 31.08.2021,
# Folder: speck_weg/app File: app.py
#

from typing import List, Dict, Union, Optional, Tuple, TYPE_CHECKING

from sqlalchemy import select, update, bindparam, func
from sqlalchemy.orm import joinedload

from ..models import (UserModel, TrainingThemeModel, TrainingProgramModel,
                      TrainingExerciseModel, TrainingProgramExerciseModel)

if TYPE_CHECKING:
    from ..db import CRUD


class Message:
    def __init__(self, title: str, text: str, level: str, informative_text: str = None,
                 button_accept_name: str = None, button_reject_name: str = None):
        # required
        self.title = title
        self.text = text
        self._level = level  # protected
        # optional
        self.informative_text = informative_text
        self.button_accept_name = button_accept_name
        self.button_reject_name = button_reject_name

        self.level = self._level

        # if the message is accepted (only possible with an accept button)
        self.accept: bool = False

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):

        if value not in ['information', 'question', 'warning', 'critical']:
            raise NotImplementedError(
                "Level must be one of 'information', 'question', 'warning' or 'critical'.")
        self._level = value

    def __repr__(self):
        return f'Message(title={self.title}, text={self.text}, level={self.level})'


class SpeckWeg:
    def __init__(self, db: 'CRUD', **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db

        # There must be one user in the database
        # self.usr = self.read_user()
        self.user = User(self.db)

        # instead of only storing the themes in the widgets, store them in lists
        self.themes: 'TrainingThemeCollection' = TrainingThemeCollection(self.db)
        self.current_tth_id: Optional[int] = None
        self.programs: 'TrainingProgramCollection' = TrainingProgramCollection(self.db)
        self.current_tpr_id: Optional[int] = None
        self.exercises: 'TrainingProgramExerciseCollection' = TrainingProgramExerciseCollection(self.db)
        self.current_tpe_id: Optional[int] = None  # training_program_exercise is unique

        # default messages
        self.messages: Dict[str, 'Message'] = dict()

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

    def exercise_delete(self):
        print('deleting', self.current_tpe_id)
        tpe_ids = [tpe.tpe_id for tpe in self.exercises.model_list]
        idx = tpe_ids.index(self.current_tpe_id)

        self.exercises.remove_exercise(tpe_id=self.current_tpe_id)
        # set another theme active
        if idx < len(self.exercises.model_list):
            # was not the last one, select the previous position
            self.current_tpe_id = self.exercises.model_list[idx].tpe_id
        elif len(self.exercises.model_list) == 0:
            self.current_tpe_id = None
        else:
            # was the last in the list -> set the current last one
            self.current_tpe_id = self.exercises.model_list[-1].tpe_id


class TrainingTheme:
    def __init__(self, db: 'CRUD',
                 tth_id: int = None, max_sequence: int = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.model: Optional['TrainingThemeModel'] = None

        if tth_id:
            stmt = select(TrainingThemeModel).where(TrainingThemeModel.tth_id == tth_id)
            res = self.db.read_one(stmt)
            self.model = res
        else:
            self.model = None
        self.max_sequence = max_sequence  # current maximum of existing training themes

    def add_theme(self, name: str, description: str):
        self.model = TrainingThemeModel(sequence=self.max_sequence+1)
        self.update_model(name, description)
        self.db.create(self.model)
        # Model saved -> clear for adding another one
        self.model = None
        self.max_sequence += 1  # if other themes are created

    def edit_theme(self, name: str, description: str):
        # updates all attributes (not the sequence, this is done from the collection)
        self.update_model(name, description)
        self.db.update()

    def update_model(self, name: str, description: str):
        self.model.name = name
        self.model.description = description


class TrainingThemeCollection:
    def __init__(self, db: 'CRUD',
                 model_list: List['TrainingThemeModel'] = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.model_list: List['TrainingThemeModel'] = []
        if model_list:
            self.model_list = model_list

    def read_themes(self):

        stmt = select(
            TrainingThemeModel).order_by(
            TrainingThemeModel.sequence).order_by(
            TrainingThemeModel.name)
        self.model_list = list(self.db.read_stmt(stmt))

    def update_sequence(self, tth_ids: List[int]):
        # stmt = update(TrainingThemeModel).where(
        #     TrainingThemeModel.tth_id == tth_id).values(sequence=i + 1)
        payload = [{'b_tth_id': tth_id, 'b_sequence': i+1} for i, tth_id in enumerate(tth_ids)]
        stmt = update(
            TrainingThemeModel).where(
            TrainingThemeModel.tth_id == bindparam('b_tth_id')).values(
            sequence=bindparam('b_sequence')
        )
        self.db.update(stmt, payload)
        self.read_themes()

        # for i, tth_id in enumerate(tth_ids):
        #     tth = next(tth for tth in self.obj_list if tth.tth_id == tth_id)
        #     tth.sequence = i + 1
        # self.db.update()

    def remove_theme(self, tth_id: int = None):  # , row: int = None):
        if tth_id:
            ids = [tth.tth_id for tth in self.model_list]
            idx = ids.index(tth_id)
            print(tth_id, ids, idx)
            tth = self.model_list.pop(idx)
            self.db.delete(tth)

            # update the sequence for the remaining themes
            ids = [tth.tth_id for tth in self.model_list]
            if ids:
                self.update_sequence(ids)


class TrainingProgram:
    def __init__(self, db: 'CRUD',
                 tpr_tth_id: int, tpr_id: int = None, max_sequence: int = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.model: Optional['TrainingProgramModel'] = None
        self.tpr_tth_id = tpr_tth_id  # parent training theme

        if tpr_id:
            stmt = select(TrainingProgramModel).where(TrainingProgramModel.tpr_id == tpr_id)
            res = self.db.read_one(stmt)
            self.model = res
        else:
            self.model = None
        self.max_sequence = max_sequence  # current maximum of existing training themes

    def add_program(self, name: str, description: str):
        self.model = TrainingProgramModel(tpr_tth_id=self.tpr_tth_id, sequence=self.max_sequence+1)
        self.update_model(name, description)
        self.db.create(self.model)
        # Model saved -> clear for adding another one
        self.model = None
        self.max_sequence += 1  # if other themes are created

    def edit_program(self, name: str, description: str):
        # updates all attributes (not the sequence, this is done from the collection)
        self.update_model(name, description)
        self.db.update()

    def update_model(self, name: str, description: str):
        self.model.name = name
        self.model.description = description


class TrainingProgramCollection:
    def __init__(self, db: 'CRUD',
                 model_list: List['TrainingProgramModel'] = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.model_list: List['TrainingProgramModel'] = []
        if model_list:
            self.model_list = model_list

    def read_programs(self, tth_id: int):

        stmt = select(
            TrainingProgramModel).where(
            TrainingProgramModel.tpr_tth_id == tth_id).order_by(
            TrainingProgramModel.sequence).order_by(
            TrainingProgramModel.name)
        self.model_list = list(self.db.read_stmt(stmt))

    def update_sequence(self, tpr_ids: List[int], tth_id: int):
        payload = [{'b_tpr_id': tpr_id, 'b_sequence': i+1} for i, tpr_id in enumerate(tpr_ids)]
        stmt = update(
            TrainingProgramModel).where(
            TrainingProgramModel.tpr_id == bindparam('b_tpr_id')).values(
            sequence=bindparam('b_sequence')
        )
        self.db.update(stmt, payload)
        self.read_programs(tth_id)

    def remove_program(self, tpr_id: int = None):
        if tpr_id:
            ids = [tpr.tpr_id for tpr in self.model_list]
            idx = ids.index(tpr_id)
            print(tpr_id, ids, idx)

            tpr = self.model_list.pop(idx)
            tth_id = tpr.tpr_tth_id
            self.db.delete(tpr)

            # update the sequence for the remaining programs
            ids = [tpr.tpr_id for tpr in self.model_list]
            if ids:
                self.update_sequence(ids, tth_id)


class TrainingProgramExerciseCollection:
    def __init__(self, db: 'CRUD',
                 model_list: List['TrainingProgramExerciseModel'] = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.model_list: List['TrainingProgramExerciseModel'] = []
        if model_list:
            self.model_list = model_list

    def read_exercises(self, tpr_id: int):
        # Read the TrainingProgramExercises (load also the related TrainingExerciseModel
        stmt = select(TrainingProgramExerciseModel).where(
            TrainingProgramExerciseModel.tpe_tpr_id == tpr_id).order_by(
            TrainingProgramExerciseModel.sequence).options(
            joinedload(TrainingProgramExerciseModel.training_exercise, innerjoin=True))
        self.model_list = list(self.db.read_stmt(stmt))

    def update_sequence(self, tpe_ids: List[int], tpr_id: int):

        payload = [{'b_tpe_id': tpe_id, 'b_sequence': i+1} for i, tpe_id in enumerate(tpe_ids)]
        stmt = update(
            TrainingProgramExerciseModel).where(
            TrainingProgramExerciseModel.tpe_id == bindparam('b_tpe_id')).values(
            sequence=bindparam('b_sequence')
        )
        self.db.update(stmt, payload)
        self.read_exercises(tpr_id)

    def remove_exercise(self, tpe_id: int = None):  # , row: int = None):
        if tpe_id:
            ids = [tpe.tpe_id for tpe in self.model_list]
            idx = ids.index(tpe_id)
            print(tpe_id, ids, idx)
            tpe = self.model_list.pop(idx)
            tpr_id = tpe.tpe_tpr_id
            self.db.delete(tpe)

            # update the sequence for the remaining themes
            ids = [tpe.tpe_id for tpe in self.model_list]
            if ids:
                self.update_sequence(ids, tpr_id)

    def check_for_last_exercise(self, tex_id) -> bool:
        """
        Counts, how often a TrainingExercise is referenced in the many2many relation

        :param tex_id:
        :return: True -> Only one reference left; False -> many references
        """
        stmt = select(func.count(TrainingProgramExerciseModel.tpe_id)).where(
            TrainingProgramExerciseModel.tpe_tex_id == tex_id)
        count = self.db.read_first(stmt)
        print('check_for_last_exercise', count)
        if count == 1:
            return True
        else:
            return False


class TrainingExercise:
    def __init__(self, db: 'CRUD', usr_id: int,
                 tpr_id: int, tex_id: int = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.model: Optional['TrainingExerciseModel'] = None
        self.parent_model, self.user_model, self.model = self.read_objects(tpr_id, usr_id, tex_id)

    @property
    def max_sequence(self) -> int:
        if self.parent_model.training_exercises:
            return max([tpe.sequence for tpe in self.parent_model.training_exercises])
        else:
            return 0

    def read_objects(self, tpr_id: int = None, usr_id: int = None, tex_id: int = None
                     ) -> Tuple['TrainingProgramModel', 'UserModel', 'TrainingExerciseModel']:
        print('reading objects', tpr_id, usr_id, tex_id)
        if not tpr_id:
            tpr_id = self.parent_model.tpr_id
        # always load the TrainingProgramExercises for getting the max_sequence
        stmt = select(TrainingProgramModel).where(
            TrainingProgramModel.tpr_id == tpr_id).options(
            joinedload(TrainingProgramModel.training_exercises))

        parent_model = self.db.read_one(stmt, unique=True)

        if not usr_id:
            usr_id = self.user_model.usr_id
        stmt = select(UserModel).where(UserModel.usr_id == usr_id)
        user_model = self.db.read_one(stmt)

        if not tex_id:
            if self.model:
                tex_id = self.model.tex_id
        if tex_id:
            stmt = select(TrainingExerciseModel).where(TrainingExerciseModel.tex_id == tex_id)
            model = self.db.read_one(stmt)
        else:
            model = None

        print('tpr model, usr model, tex model')
        print(parent_model, user_model, model)
        return parent_model, user_model, model

    def add_exercise(self, tex_usr_id: int, name: str, description: str,
                     baseline_sets: int,  baseline_repetitions: int,
                     baseline_weight: float, baseline_duration: float):

        self.model = TrainingExerciseModel()
        self.update_model(tex_usr_id, name, description, baseline_sets,
                          baseline_repetitions, baseline_weight, baseline_duration)
        # Add the many2many relation
        tpe = TrainingProgramExerciseModel(sequence=self.max_sequence+1)
        tpe.training_program = self.parent_model
        tpe.training_exercise = self.model

        self.db.create(self.model)
        # Model saved -> clear for adding another one
        self.model = None
        # self.max_sequence += 1  # if other themes are created

    def edit_exercise(self, tex_usr_id: int, name: str, description: str,
                      baseline_sets: int,  baseline_repetitions: int,
                      baseline_weight: float, baseline_duration: float):

        # updates all attributes (not the sequence, this is done from the collection)
        self.update_model(tex_usr_id, name, description, baseline_sets,
                          baseline_repetitions, baseline_weight, baseline_duration)
        self.db.update()

    def update_model(self, tex_usr_id: int, name: str, description: str,
                     baseline_sets: int,  baseline_repetitions: int,
                     baseline_weight: float, baseline_duration: float):
        self.model.tex_usr_id = tex_usr_id
        self.model.name = name
        self.model.description = description
        self.model.baseline_sets = baseline_sets
        self.model.baseline_repetitions = baseline_repetitions
        self.model.baseline_weight = baseline_weight
        self.model.baseline_duration = baseline_duration


class TrainingExerciseCollection:
    # Used for the import of an exercise to a program
    def __init__(self, db: 'CRUD',
                 tpr_id: int, usr_id: int, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db

        self.current_tex_id = None

        # read the parent / user model
        stmt = select(TrainingProgramModel).where(TrainingProgramModel.tpr_id == tpr_id)
        self.parent_model: 'TrainingProgramModel' = self.db.read_one(stmt)
        stmt = select(UserModel).where(UserModel.usr_id == usr_id)
        self.user_model: 'UserModel' = self.db.read_one(stmt)

        # read all available training exercises
        stmt = select(TrainingExerciseModel).order_by(TrainingExerciseModel.name)
        self.model_list: List['TrainingExerciseModel'] = list(self.db.read_stmt(stmt))
        print('initializing TrainingExerciseCollection', len(self.model_list))

    # def read_exercises(self, tpr_id: int):
    #     # Read the TrainingProgramExercises (load also the related TrainingExerciseModel
    #     stmt = select(TrainingProgramExerciseModel).where(
    #         TrainingProgramExerciseModel.tpe_tpr_id == tpr_id).order_by(
    #         TrainingProgramExerciseModel.sequence).options(
    #         joinedload(TrainingProgramExerciseModel.training_exercise, innerjoin=True))
    #     self.model_list = list(self.db.read_stmt(stmt))

    @property
    def current_model(self):
        return next(tex for tex in self.model_list if tex.tex_id == self.current_tex_id)

    def import_exercise(self):

        if self.parent_model.training_exercises:
            max_sequence = max([tpr.sequence for tpr in self.parent_model.training_exercises])
        else:
            max_sequence = 0
        tpe = TrainingProgramExerciseModel(sequence=max_sequence + 1)
        tpe.training_exercise = self.current_model
        tpe.training_program = self.parent_model

        self.db.update()
        # self.db.create(tpe) ?


class User:
    def __init__(self, db: 'CRUD',
                 usr_id: int = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.model: Optional['UserModel'] = None

        # initially search for the current user (if not given)
        if usr_id:
            stmt = select(UserModel).where(UserModel.usr_id == usr_id)
            res = self.db.read_one(stmt)
            self.model = res
        else:
            self.model = None
        if not usr_id:
            self.model = self.read_current_user()

    def read_current_user(self) -> Union['UserModel', None]:
        # selects the first entry in the user table
        stmt = select(UserModel)
        return self.db.read_first(stmt)

    def update_usr_attributes(self, name: str, weight: float):
        # update all attributes

        self.model.name = name
        self.model.weight = weight

    def save_user(self, name: str, weight: float):
        if self.model:
            self.update_usr_attributes(name, weight)
            self.db.update()

        else:
            self.model = UserModel()
            self.update_usr_attributes(name, weight)
            self.db.create(self.model)
