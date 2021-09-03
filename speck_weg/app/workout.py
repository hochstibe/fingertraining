# fingertraining
# Stefan Hochuli, 31.08.2021,
# Folder: speck_weg/app File: workout.py
#

from typing import List, Optional, Union, Tuple, Dict

from sqlalchemy import select

from .app import Message
from ..db import CRUD
from ..models import TrainingProgramModel, TrainingExerciseModel, WorkoutSessionModel, WorkoutExerciseModel, UserModel


class Workout:
    def __init__(self, db: 'CRUD', parent_tpr: 'TrainingProgramModel',
                 obj: 'WorkoutSessionModel' = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db

        self.wse: Optional['WorkoutSessionModel'] = obj
        self.parent_tpr: 'TrainingProgramModel' = parent_tpr
        # List of [planned exercise, [logged sets of the exercise]]
        self.exercises: List[List['TrainingExerciseModel', List[Optional[WorkoutExerciseModel]]]] = []

        # default messages
        self.messages: Dict[str, 'Message'] = dict()

        title = 'Kein User vorhanden.'
        text = 'Bitte zuerst einen User erstellen.'
        self.messages['no_user'] = Message(title, text, 'information')

        title = 'Session löschen'
        text = 'Die Session wird geschlossen und gelöscht. ' \
               'Alle gespeicherten Übungen werden ebenfalls gelöscht.'
        self.messages['delete_session'] = Message(title, text, 'question',
                                                  button_accept_name='Löschen')

        # Get the current user
        stmt = select(UserModel)
        self.usr: 'UserModel' = self.db.read_first(stmt)

        # Set the starting position
        self.current_pos: int = -1
        self.current_set: int = -1
        # Default values for the current exercise (start / end -> None)
        self.baseline_weight: Optional[float] = None
        self.baseline_duration: Optional[float] = None

        if self.wse:
            # edit mode
            pass
        else:
            # new mode
            self.wse = WorkoutSessionModel(wse_tpr_id=self.parent_tpr.tpr_id)
            self.db.create(self.wse)

        # Generate a list for all exercises (pairs for planned an done exercises)
        self.exercises = [
            [tpe.training_exercise, [None for _ in range(tpe.training_exercise.baseline_sets)]]
            for tpe in self.parent_tpr.training_exercises
        ]

    @property
    def current_exercise(self) -> Union[
        Tuple[
            'TrainingExerciseModel',
            Optional['WorkoutExerciseModel']
        ],
        None
    ]:
        """
        :return: Current TrainingExercise,  current WorkoutExercise (if already saved)
        """
        if self.current_pos in range(len(self.exercises)):
            tex, wexes = self.exercises[self.current_pos]
            wex = wexes[self.current_set - 1]
            print(tex, wex)
            return tex, wex
        else:
            print('out of range', self.current_pos, len(self.exercises))
            return None

    @current_exercise.setter
    def current_exercise(self, wex: 'WorkoutExerciseModel'):
        if self.current_pos in range(len(self.exercises)):
            tex, wexes = self.exercises[self.current_pos]
            wexes[self.current_set - 1] = wex

    def save(self, repetitions: int, weight: float, duration: int, comment: str):
        if self.current_pos == -1 or self.current_pos == len(self.exercises):
            # start / stop
            self.save_session(comment)
        else:
            self.save_exercise(repetitions, weight, duration, comment)

    def delete(self):
        if self.current_pos == -1 or self.current_pos == len(self.exercises):
            # start or end: delete the session
            # UI
            # ask message -> clicked
            # delete()
            # reject()
            if self.wse.workout_exercises:
                self.db.delete(self.wse.workout_exercises)
            self.db.delete(self.wse)
        else:
            # delete the exercise
            tex, wex = self.current_exercise
            self.db.delete(wex)

    def save_session(self, comment: str):
        print('saving session (comment)')
        # UI
        # widgets2object
        # save the comment
        print(self.wse, comment)
        self.wse.comment = comment
        print(self.wse)
        print('dirty', self.wse in self.db.session.dirty)
        self.db.update()
        print('dirty', self.wse in self.db.session.dirty)

        # UI
        # Update widgets after saving??
        # score = self.assess_session()
        # self.assess_session_set_text(score)

    def update_wex(self, wex: 'WorkoutExerciseModel', repetitions: int, weight: Optional[float],
                   duration: Optional[int], comment: Optional[str]):

        wex.sequence = self.current_pos + 1,  # the position equals the sequence in the tpe
        wex.set = self.current_set
        wex.repetitions = repetitions
        if self.baseline_weight:
            if not weight:
                raise ValueError('The Exercises requires a weight')
            wex.weight = weight
        if self.baseline_duration:
            if not duration:
                raise ValueError('The Exercises requires a duration')
            wex.duration = duration
        wex.comment = comment

    def save_exercise(self, repetitions: int, weight: float, duration: int, comment: str):
        # UI
        # - updated object from widgets
        # - save

        tex, wex = self.current_exercise
        print('saving exercise')

        if wex:
            print('  existing', wex)
            self.update_wex(wex, repetitions, weight, duration, comment)
            # The exercise already exists in the database
            self.db.update()

        else:
            # Create a new Object, add the relations
            wex = WorkoutExerciseModel()
            wex.training_exercise = tex
            wex.workout_session = self.wse
            self.update_wex(wex, repetitions, weight, duration, comment)
            print(' ', wex)
            self.db.create(wex)

        # Add the tex to the wex
        self.current_exercise = wex
        print(self.current_exercise)

        # assess the score of the exercise
        # score = self.assess_exercise(tex, wex)

        # UI
        # update widgets or only the score
        # self.assess_exercise_set_text(score)

    def previous_exercise(self) -> Union[str, Tuple['TrainingExerciseModel', 'WorkoutExerciseModel']]:
        print('previous exercise or set')
        # minimum position: -1
        go2start = False

        if len(self.exercises) == self.current_pos:
            # end position, go to last set of the last exercise, current_set was not changed
            self.current_pos -= 1
            tex, wex = self.current_exercise
            self.current_set = tex.baseline_sets

        elif 0 == self.current_pos:
            # first exercise
            if self.current_set == 1:
                # go to start position
                self.current_pos -= 1
                go2start = True
            else:
                # previous set of the first exercise
                self.current_set -= 1

        elif self.current_pos > 0:
            if self.current_set > 1:
                # previous set of the current exercise
                print('previous set of the current exercise')
                self.current_set -= 1
            else:
                # last set of the previous exercise
                print('last set of the previous exercise')
                self.current_pos -= 1
                tex, wex = self.current_exercise
                self.current_set = tex.baseline_sets

        if go2start:
            return 'start'
        else:
            return self.current_exercise

    def next_exercise(self) -> Union[str, Tuple['TrainingExerciseModel', 'WorkoutExerciseModel']]:
        print('next exercise')
        # maximum position: len(self.exercises)
        go2end = False

        if self.current_pos == len(self.exercises) - 1:
            # last exercise
            tex, wex = self.current_exercise
            if self.current_set == tex.baseline_sets:
                # go to end position
                print('go to end position')
                self.current_pos += 1
                go2end = True
            else:
                # go to the next set of the exercise
                print('go to the next set of the last exercise')
                self.current_set += 1

        elif -1 == self.current_pos:
            # start position, go to first set of the first exercise
            print('start position, go to first set of the first exercise')
            self.current_pos += 1
            self.current_set = 1
        elif self.current_pos < len(self.exercises):
            tex, wex = self.current_exercise
            if self.current_set < tex.baseline_sets:
                # next set of the current exercise
                print('next set of the current exercise')
                self.current_set += 1
            else:
                # first set of the next exercise
                print('first set of the next exercise')
                self.current_pos += 1
                self.current_set = 1

        if go2end:
            return 'end'
        else:
            return self.current_exercise

    def calc_ratio(self, weight: float) -> float:
        return weight / self.baseline_weight

    def calc_weight(self, ratio: float) -> float:
        return ratio * self.baseline_weight

    def assess(self) -> Optional[float]:
        if self.current_pos == -1 or self.current_pos == len(self.exercises):
            score = self.assess_session()
        else:
            tex, wex = self.current_exercise
            score = self.assess_exercise(tex, wex)

        return score

    def assess_exercise(self, tex: 'TrainingExerciseModel', wex: Optional['WorkoutExerciseModel']
                        ) -> Optional[float]:

        if wex:
            score = wex.repetitions / tex.baseline_repetitions
            if self.baseline_weight:  # tex.baseline_weight or usr.weight
                score *= wex.weight / self.baseline_weight
            if self.baseline_duration:
                score *= wex.duration / self.baseline_duration
            return score

        return None  # if start / end or no wex yet

    def assess_session(self) -> float:

        score = 1
        skipped = 0
        print(self.exercises)
        for tex, wexes in self.exercises:
            tex_score = 1
            wex_skipped = 0
            for i, wex in enumerate(wexes):
                if wex:
                    if i < tex.baseline_sets:
                        tex_score *= self.assess_exercise(tex, wex)
                    else:  # additional sets increase with +
                        tex_score += self.assess_exercise(tex, wex) / tex.baselin_sets

                else:  # no workout saved for the set
                    print('no workout saved for the set')
                    # print(tex_score, tex_score / tex.baseline_sets)
                    # tex_score -= tex_score / tex.baseline_sets
                    wex_skipped += 1
            tex_score -= tex_score * wex_skipped / len(wexes)
            if tex_score == 0:
                print('no exercise saved for tex', tex)
                skipped += 1
            else:
                score *= tex_score

        score -= score * skipped / len(self.exercises)

        return score

    def update_baseline(self):
        if self.current_pos <= -1:
            self.current_pos = -1
            self.baseline_weight = None
            self.baseline_duration = None
        elif self.current_pos >= len(self.exercises):
            self.current_pos = len(self.exercises)
            self.baseline_weight = None
            self.baseline_duration = None
        else:
            tex, wex = self.current_exercise

            # set default values for weight / duration
            if tex.baseline_weight:
                self.baseline_weight = tex.baseline_weight
            elif tex.tex_usr_id:
                self.baseline_weight = self.usr.weight
            else:
                self.baseline_weight = None
            if tex.baseline_duration:
                self.baseline_duration = tex.baseline_duration
            else:
                self.baseline_duration = None
