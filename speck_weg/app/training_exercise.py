# fingertraining
# Stefan Hochuli, 09.09.2021,
# Folder: speck_weg/app File: training_exercise.py
#

from typing import List, Optional, Tuple, TYPE_CHECKING

from sqlalchemy import select, update, bindparam, func
from sqlalchemy.orm import joinedload

from ..models import (TrainingProgramExerciseModel, TrainingProgramModel,
                      UserModel, TrainingExerciseModel)

if TYPE_CHECKING:
    from ..db import CRUD


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

    def remove_exercise(self, tpe_id: int = None, child: bool = False):
        if tpe_id:
            ids = [tpe.tpe_id for tpe in self.model_list]
            idx = ids.index(tpe_id)
            print(tpe_id, ids, idx)
            tpe = self.model_list.pop(idx)
            tpr_id = tpe.tpe_tpr_id
            if child:
                self.db.delete([tpe.training_exercise, tpe])
            else:
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
        self.model.baseline_custom_weight = baseline_weight
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
