# fingertraining
# Stefan Hochuli, 09.09.2021,
# Folder: speck_weg/app File: workout_exercise.py
#

from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..models import WorkoutSessionModel, WorkoutExerciseModel, TrainingExerciseModel

if TYPE_CHECKING:
    from ..db import CRUD


# class WorkoutExercise:
#     # Used for the import of an exercise to a program
#     def __init__(self, db: 'CRUD',
#                  wse_id: int, tex_id, usr_id: int, wex_id: int = None, **kwargs):
#         # Additional arguments are passed to next inheritance
#         super().__init__(**kwargs)
#
#         self.db = db
#
#         # WorkoutSession
#         stmt = select(WorkoutSessionModel).where(WorkoutSessionModel.wse_id == wse_id)
#         self.parent_wse_model = self.db.read_one(stmt)
#         # TrainingExercise
#         stmt = select(TrainingExerciseModel).where(TrainingExerciseModel.tex_id == tex_id)
#         self.parent_tex_model = self.db.read_one(stmt)
#         # User
#         stmt = select(UserModel).where(UserModel.usr_id == usr_id)
#         self.usr_model = self.db.read_one(stmt)
#
#         # WorkoutExercise
#         self.model: Optional['WorkoutExerciseModel'] = None
#         if wex_id:
#             stmt = select(WorkoutExerciseModel).where(WorkoutExerciseModel.wex_id == wex_id)
#             self.model = self.db.read_one(stmt)
#
#     def add_exercise(self, sequence: int, n_set: int, repetitions: int,
#                      weight: float, duration: float, comment: str):
#         self.model = WorkoutExerciseModel()
#         self.model.training_exercise = self.parent_tex_model
#         self.model.workout_session = self.parent_wse_model
#
#         self.update_model(sequence, n_set, repetitions, weight, duration, comment)
#         self.db.update()  # should insert the new model
#
#     def edit_exercise(self, sequence: int, n_set: int, repetitions: int,
#                       weight: float, duration: float, comment: str):
#         self.update_model(sequence, n_set, repetitions, weight, duration, comment)
#         self.db.update()
#
#     def remove_exercise(self):
#         self.db.delete(self.model)
#         self.model = None
#
#     def update_model(self, sequence: int, n_set: int, repetitions: int,
#                      weight: float, duration: float, comment: str):
#
#         self.model.sequence = sequence
#         self.model.set = n_set
#         self.model.repetitions = repetitions
#         self.model.weight = weight
#         self.model.duration = duration
#         self.model.comment = comment


class WorkoutExerciseSet:
    def __init__(self, db: 'CRUD', wse_id: int, tex_id):

        self.db = db
        # WorkoutSession
        stmt = select(WorkoutSessionModel).where(WorkoutSessionModel.wse_id == wse_id)
        self.wse_model: 'WorkoutSessionModel' = self.db.read_one(stmt)
        # TrainingExercise
        stmt = select(TrainingExerciseModel).where(
            TrainingExerciseModel.tex_id == tex_id).options(
            joinedload(TrainingExerciseModel.user)
        )
        self.tex_model: 'TrainingExerciseModel' = self.db.read_one(stmt)

        self.wex_model_list: List[Optional['WorkoutExerciseModel']] = [
            None for _ in range(self.tex_model.baseline_sets)
        ]
        # Todo: select the models and replace None (if they exist -> for editing)

        # Set the baseline values for weight / duration
        if self.tex_model.baseline_weight:
            self.baseline_weight = self.tex_model.baseline_weight
        elif self.tex_model.user:
            self.baseline_weight = self.tex_model.user.weight
        else:
            self.baseline_weight = None

    def add_exercise(self, sequence: int, n_set: int, repetitions: int,
                     weight: float, duration: float, comment: str):
        model = WorkoutExerciseModel()
        model.training_exercise = self.tex_model
        model.workout_session = self.wse_model
        model.sequence = sequence
        model.set = n_set + 1
        self.wex_model_list[n_set] = model

        self.update_model(n_set, repetitions, weight, duration, comment)
        self.db.update()  # should insert the new model

    def edit_exercise(self, n_set: int, repetitions: int,
                      weight: float, duration: float, comment: str):
        self.update_model(n_set, repetitions, weight, duration, comment)
        self.db.update()

    def remove_exercise(self, n_set):
        model = self.wex_model_list[n_set]
        self.db.delete(model)
        self.wex_model_list[n_set] = None

    def update_model(self, n_set: int, repetitions: int,
                     weight: float, duration: float, comment: str):

        model = self.wex_model_list[n_set]

        # Sequence and set is not updated
        model.repetitions = repetitions
        if self.baseline_weight:
            model.weight = weight
        if self.tex_model.baseline_duration:
            model.duration = duration
        model.comment = comment

    def assess_set(self) -> float:
        # Calculate the score for the TrainingExercise including all sets of the exercise
        score = 1
        wex_skipped = 0
        for i, wex in enumerate(self.wex_model_list):
            if wex:
                # A WorkoutExercise was saved for this set
                if i < self.tex_model.baseline_sets:
                    score *= self.assess_exercise(i)
                else:  # additional sets increase with +
                    score += self.assess_exercise(i) / self.tex_model.baseline_sets
            else:  # no workout saved for this set
                print('no workout saved for the set')
                wex_skipped += 1
        # reduce for skipped sets
        score -= score * wex_skipped / len(self.wex_model_list)
        # all skipped --> score = 0

        return score

    def assess_exercise(self, n_set: int) -> Optional[float]:
        # actually belongigg to WorkoutExercise,
        # but the wex_list is a list of models and not of WorkoutExercise (to reduce complexity?)
        wex = self.wex_model_list[n_set]
        if wex:
            score = wex.repetitions / self.tex_model.baseline_repetitions
            if self.baseline_weight:  # tex.baseline_weight or usr.weight
                score *= wex.weight / self.baseline_weight
            if self.tex_model.baseline_duration:
                score *= wex.duration / self.tex_model.baseline_duration
            return score
        else:
            # No wex yet
            return None
