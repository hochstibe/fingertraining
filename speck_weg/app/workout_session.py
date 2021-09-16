# fingertraining
# Stefan Hochuli, 09.09.2021,
# Folder: speck_weg/app File: workout_session.py
#

from typing import List, Tuple, Optional, Union, TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .workout_exercise import WorkoutExerciseSet
from ..models import (TrainingProgramModel, WorkoutSessionModel)

if TYPE_CHECKING:
    from ..db import CRUD


class WorkoutSession:
    def __init__(self, db: 'CRUD',
                 tpr: Union[int, 'TrainingProgramModel'] = None,
                 wse: Union[int, 'WorkoutSessionModel'] = None, **kwargs):
        """
        Either the  the WorkoutSession is given (TrainingProgram is fetched from the orm)
        or the TrainingProgram is given (no Workout session yet)

        :param db:
        :param tpr:
        :param wse:
        :param kwargs:
        """
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db

        # read the objects from the database
        self.model = None
        if isinstance(wse, WorkoutSessionModel):
            self.model = wse
            self.tpr_model = wse.training_program
        elif isinstance(tpr, TrainingProgramModel):
            self.tpr_model = tpr
            self.model = None
        else:
            # Load from the ids
            self.tpr_model, self.model = self.read_objects(tpr, wse)

        if not self.model:
            # Start a new session
            self.add_session()

        # List of [planned exercise, [logged sets of the exercise]]
        # self.exercises: List[Tuple['TrainingExerciseModel',
        #                            List[Optional[WorkoutExercise]]]] = []
        # Generate a list for all exercises (pairs for planned an done exercises)
        self.exercises = [WorkoutExerciseSet(db, self.model.wse_id, tpe.tpe_tex_id)
                          for tpe in self.tpr_model.training_exercises]

        # for tpe in self.tpr_model.training_exercises:
        #     self.exercises.append(
        #       (tpe.training_exercise, [None for _ in range(tpe.training_exercise.baseline_sets)])
        #     )

    @property
    def wex_saved(self):
        wex_models = [wex for wex_set in self.exercises
                      for wex in wex_set.wex_model_list]
        if any(wex_models):
            return True
        else:
            return False

    def read_objects(self, tpr_id: int = None, wse_id: int = None
                     ) -> Tuple['TrainingProgramModel', Optional['WorkoutSessionModel']]:
        # Parent
        # if not tpr_id:
        #     tpr_id = self.tpr_model.tpr_id
        # also load the training theme (name is needed for the gui
        # stmt = select(TrainingProgramModel).where(TrainingProgramModel.tpr_id == tpr_id).options(
        #     joinedload(TrainingProgramModel.training_theme, innerjoin=True)
        # )
        # parent_model = self.db.read_one(stmt)

        # if not wse_id:
        #     if self.model:
        #         wse_id = self.model.wse_id
        if wse_id:
            stmt = select(WorkoutSessionModel).where(WorkoutSessionModel.wse_id == wse_id)
            model = self.db.read_one(stmt)
            tpr_id = model.wse_tpr_id
            stmt = select(TrainingProgramModel).where(
                TrainingProgramModel.tpr_id == tpr_id).options(
                joinedload(TrainingProgramModel.training_theme, innerjoin=True))
            parent_model = self.db.read_one(stmt)
        # else:
        #     model = None
        elif tpr_id:
            # also load the training theme (name is needed for the gui
            stmt = select(TrainingProgramModel).where(
                TrainingProgramModel.tpr_id == tpr_id).options(
                joinedload(TrainingProgramModel.training_theme, innerjoin=True))
            parent_model = self.db.read_one(stmt)
            model = None
        else:
            raise ValueError('Either wse_id or tpr_id must be given')
        return parent_model, model

    # def read_exercises(self):
    #     stmt = select(WorkoutExerciseModel)
    #     for tpe in self.tpr_model.training_exercises:

    def add_session(self):
        self.model = WorkoutSessionModel()
        self.model.training_program = self.tpr_model
        self.db.create(self.model)

    def edit_session(self, comment: str):
        self.model.comment = comment
        self.db.update()

    def remove_session(self):
        # Deletes the session and all the exercises

        # Create a list of all existing wex models
        # model_list = []
        # for wex_set in self.workout_session.exercises:
        #     for wex in wex_set.wex_model_list:
        #         if wex:
        #             model_list.append(wex)

        model_list = [wex for wex_set in self.exercises
                      for wex in wex_set.wex_model_list if wex]
        # Add the wse to the list
        if self.model:
            model_list.append(self.model)
        self.db.delete(model_list)

        # remove from the lists
        self.model = None
        for wex_set in self.exercises:
            wex_set.wex_model_list = [None for _ in wex_set.wex_model_list]
        print('models after delete:', self.model, [wex_set.wex_model_list
                                                   for wex_set in self.exercises])

    def assess_session(self) -> float:
        score = 1
        skipped = 0
        print(self.exercises)
        for wex_set in self.exercises:

            wex_set_score = wex_set.assess_set()
            if wex_set_score == 0:
                print('no exercise saved for tex', wex_set.tex_model)
                skipped += 1
            else:
                score *= wex_set_score

        score -= score * skipped / len(self.exercises)

        return score


class WorkoutSessionCollection:
    def __init__(self, db: 'CRUD',
                 tpr_id: int = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.workout_list: List['WorkoutSession'] = []

    def read_sessions(self, tpr_id: int = None, tth_id: int = None):

        if tpr_id:
            stmt = select(WorkoutSessionModel).where(
                WorkoutSessionModel.wse_tpr_id == tpr_id).order_by(
                WorkoutSessionModel.date).options(
                joinedload(WorkoutSessionModel.training_program, innerjoin=True)
            )
        elif tth_id:
            stmt = select(WorkoutSessionModel).join(WorkoutSessionModel.training_program).where(
                TrainingProgramModel.tpr_tth_id == tth_id).options(
                joinedload(WorkoutSessionModel.training_program, innerjoin=True)
            )
        else:
            stmt = select(WorkoutSessionModel).order_by(
                WorkoutSessionModel.date).options(
                joinedload(WorkoutSessionModel.training_program, innerjoin=True)
            )

        model_list = list(self.db.read_stmt(stmt))
        self.workout_list = [WorkoutSession(self.db, wse=wse) for wse in model_list]
