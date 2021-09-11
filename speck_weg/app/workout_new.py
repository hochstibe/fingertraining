# fingertraining
# Stefan Hochuli, 10.09.2021,
# Folder: speck_weg/app File: workout_new.py
#

from typing import Optional, Union, Dict, TYPE_CHECKING

from .app import Message
from ..db import CRUD
from .workout_session import WorkoutSession

if TYPE_CHECKING:
    from .workout_exercise import WorkoutExerciseSet


class Workout:
    def __init__(self, db: 'CRUD', tpr_id: int,
                 wse_id: int = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.workout_session = WorkoutSession(db, tpr_id, wse_id)

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

        # Set the starting position
        # both, the position and the set equals the position in the respective list
        # in the database, the values start with 1
        # --> always add +1 for persisting the position or set in the database
        self.current_pos: int = -1  # position in WorkoutSession.exercises
        self.current_set: int = -1  # position in WorkoutExerciseSet.wex_model_list
        # Default values for the current exercise (start / end -> None)
        # self.baseline_weight: Optional[float] = None
        # self.baseline_duration: Optional[float] = None

    @property
    def current_exercise_set(self) -> Union['WorkoutExerciseSet', None]:
        if self.current_pos in range(len(self.workout_session.exercises)):
            return self.workout_session.exercises[self.current_pos]
        else:
            print('out of range', self.current_pos, len(self.workout_session.exercises))
            return None

    # @property
    # def current_exercise(self) -> Union[
    #     Tuple[
    #         'TrainingExerciseModel',
    #         Optional['WorkoutExerciseModel']
    #     ],
    #     None
    # ]:
    #     """
    #     :return: Current TrainingExercise,  current WorkoutExercise (if already saved)
    #     """
    #     if self.current_pos in range(len(self.workout_session.exercises)):
    #         # exercise = self.workout_session.exercises[self.current_pos]
    #         tex = self.current_exercise_set.tex_model
    #         wex = self.current_exercise_set.wex_model_list[self.current_set]
    #
    #         # tex, wexes = self.exercises[self.current_pos]
    #         # wex = wexes[self.current_set - 1]
    #         print(tex, wex)
    #         return tex, wex
    #     else:
    #         print('out of range', self.current_pos, len(self.workout_session.exercises))
    #         return None
    #
    # @current_exercise.setter
    # def current_exercise(self, asdf):
    #     if self.current_pos in range(len(self.workout_session.exercises)):
    #         # exercise_set = self.workout_session.exercises[self.current_pos]
    #         self.current_exercise_set.add_exercise()
    #         # Todo: add attributes
    #         # tex, wexes = self.exercises[self.current_pos]
    #         # wexes[self.current_set - 1] = wex

    def save(self, comment: str,  # comment is for both: session and exercise
             repetitions: int = None,
             weight: float = None, duration: float = None):
        # all attributes from the widgets are given -> not necessary for the session...
        if self.current_pos == -1 or self.current_pos == len(self.workout_session.exercises):
            # start / stop
            self.workout_session.edit_session(comment)
        else:
            if self.current_exercise_set.wex_model_list[self.current_set]:
                # edit the model
                self.current_exercise_set.edit_exercise(
                    n_set=self.current_set,   # only for accessing the exercise
                    repetitions=repetitions, weight=weight,
                    duration=duration, comment=comment
                )
            else:
                # new model
                # the position equals the sequence in the tpe
                self.current_exercise_set.add_exercise(
                    sequence=self.current_pos + 1, n_set=self.current_set,
                    repetitions=repetitions, weight=weight,
                    duration=duration, comment=comment
                )

    def delete(self):
        if self.current_pos == -1 or self.current_pos == len(self.workout_session.exercises):
            self.workout_session.remove_session()

        else:
            self.current_exercise_set.remove_exercise(self.current_set)

    def previous_exercise(self):
        print('previous exercise or set')
        # minimum position: -1

        if len(self.workout_session.exercises) == self.current_pos:
            # end position, go to last set of the last exercise, current_set was not changed
            self.current_pos -= 1
            # tex, wex = self.current_exercise
            self.current_set = self.current_exercise_set.tex_model.baseline_sets - 1
            # If you can add more sets than in the baseline -> go to len(wex_model_list)-1

        elif 0 == self.current_pos:
            # first exercise
            if self.current_set == 0:
                # go to start position
                self.current_pos -= 1
            else:
                # previous set of the first exercise
                self.current_set -= 1

        elif self.current_pos > 0:
            if self.current_set > 0:
                # previous set of the current exercise
                print('previous set of the current exercise')
                self.current_set -= 1
            else:
                # last set of the previous exercise
                print('last set of the previous exercise')
                self.current_pos -= 1
                self.current_set = self.current_exercise_set.tex_model.baseline_sets - 1
        else:
            # if it is on start position (-1), nothing happens
            # if it is higher than len(self.workout_session.exercises) -> error?
            pass

    def next_exercise(self):
        print('next exercise')
        # maximum position: len(self.workout_session.exercises)

        if self.current_pos == len(self.workout_session.exercises) - 1:
            # last exercise
            if self.current_set == self.current_exercise_set.tex_model.baseline_sets - 1:
                # last set -> go to end position
                print('go to end position')
                self.current_pos += 1
                # self.current_set += 1 --> does not matter -> remove some if/else
            else:
                # go to the next set of the exercise
                print('go to the next set of the last exercise')
                self.current_set += 1

        elif -1 == self.current_pos:
            # start position, go to first set of the first exercise
            print('start position, go to first set of the first exercise')
            self.current_pos += 1
            self.current_set = 0
        elif self.current_pos < len(self.workout_session.exercises):
            if self.current_set < self.current_exercise_set.tex_model.baseline_sets - 1:
                # next set of the current exercise
                print('next set of the current exercise')
                self.current_set += 1
            else:
                # first set of the next exercise
                print('first set of the next exercise')
                self.current_pos += 1
                self.current_set = 0

    def calc_ratio(self, weight: float) -> float:
        return weight / self.current_exercise_set.baseline_weight

    def calc_weight(self, ratio: float) -> float:
        return ratio * self.current_exercise_set.baseline_weight

    def assess(self) -> Optional[float]:
        if self.current_pos == -1 or self.current_pos == len(self.workout_session.exercises):
            # assess the session (all sets of all exercise)
            # no exercises yet -> 0
            score = self.workout_session.assess_session()
        else:
            # asses the current set of the current exercise
            # no wex yet -> False
            score = self.current_exercise_set.assess_exercise(self.current_set)

        return score
