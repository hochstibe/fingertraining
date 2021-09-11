# fingertraining
# Stefan Hochuli, 09.09.2021,
# Folder: speck_weg/app File: workout_session.py
#

from typing import Tuple, Optional, TYPE_CHECKING

from sqlalchemy import select

from .workout_exercise import WorkoutExerciseSet
from ..models import (TrainingProgramModel, WorkoutSessionModel)

if TYPE_CHECKING:
    from ..db import CRUD


class WorkoutSession:
    def __init__(self, db: 'CRUD',
                 tpr_id: int, wse_id: int = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db

        # read the objects from the database

        self.tpr_model, self.model = self.read_objects(tpr_id, wse_id)

        if not self.model:
            # Start a new session
            self.add_session()

        # List of [planned exercise, [logged sets of the exercise]]
        # self.exercises: List[Tuple['TrainingExerciseModel',
        #                            List[Optional[WorkoutExercise]]]] = []
        # Generate a list for all exercises (pairs for planned an done exercises)
        self.exercises = [WorkoutExerciseSet(db, wse_id, tpe.tpe_tex_id)
                          for tpe in self.tpr_model.training_exercises]

        # for tpe in self.tpr_model.training_exercises:
        #     self.exercises.append(
        #       (tpe.training_exercise, [None for _ in range(tpe.training_exercise.baseline_sets)])
        #     )

    def read_objects(self, tpr_id: int = None, wse_id: int = None
                     ) -> Tuple['TrainingProgramModel', Optional['WorkoutSessionModel']]:
        # Parent
        if not tpr_id:
            tpr_id = self.tpr_model.tpr_id
        stmt = select(TrainingProgramModel).where(TrainingProgramModel.tpr_id == tpr_id)
        parent_model = self.db.read_one(stmt)

        if not wse_id:
            if self.model:
                wse_id = self.model.wse_id
        if wse_id:
            stmt = select(WorkoutSessionModel).where(WorkoutSessionModel.wse_id == wse_id)
            model = self.db.read_one(stmt)
        else:
            model = None

        return parent_model, model

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
        model_list.append(self.model)
        self.db.delete(model_list)

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
