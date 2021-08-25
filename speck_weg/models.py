# fingertraining
# Stefan Hochuli, 14.07.2021,
# Folder: speck_weg File: models.py
#

from sqlalchemy.orm import declarative_base, relationship
from .tables import tth_table, tpr_table, tpr_tex_table, tex_table, wse_table, wex_table, usr_table

Base = declarative_base()


class TrainingTheme(Base):
    # table definitions
    __table__ = tth_table

    # orm definitions
    training_programs = relationship('TrainingProgram', back_populates='training_theme')

    def __repr__(self):
        return f'TrainingTheme(' \
               f'tth_id={self.tth_id!r}, name={self.name!r})'


class TrainingProgram(Base):
    # table definitions
    __table__ = tpr_table

    # orm definitions
    training_theme = relationship('TrainingTheme', back_populates='training_programs')
    training_exercises = relationship('TrainingExercise', secondary=tpr_tex_table,
                                      back_populates='training_programs')
    workout_sessions = relationship('WorkoutSession', back_populates='training_program')

    def __repr__(self):
        return f'TrainingProgram(' \
               f'tpr_id={self.tth_id!r}, name={self.name!r})'


class TrainingExercise(Base):
    # table definitions
    __table__ = tex_table

    # orm definitions
    training_programs = relationship('TrainingProgram', secondary=tpr_tex_table,
                                     back_populates='training_exercises')
    workout_exercises = relationship('WorkoutExercise', back_populates='training_exercise')

    def __repr__(self):
        return f'TrainingExercise(' \
               f'tex_id={self.tex_id!r}, name={self.name!r})'


class WorkoutSession(Base):
    # table definitions
    __table__ = wse_table

    # orm definitions
    training_program = relationship('TrainingProgram', back_populates='workout_sessions')
    workout_exercises = relationship('WorkoutExercise', back_populates='workout_session')

    def __repr__(self):
        return f'WorkoutSession(' \
               f'wse_id=({self.wse_id!r}, tse_tpr_id={self.wse_tpr_id}, date={self.date})'


class WorkoutExercise(Base):
    # table definitions
    __table__ = wex_table

    # orm definitions
    workout_session = relationship('WorkoutSession', back_populates='workout_exercises')
    training_exercise = relationship('TrainingExercise', back_populates='workout_exercises')

    def __repr__(self):
        return f'WorkoutExercise(' \
               f'wex_id={self.wex_id}, wex_wse_id={self.wex_wse_id}, wex_tex_id={self.wex_tex_id})'


class User(Base):

    # table definitions
    __table__ = usr_table

    def __repr__(self):
        return f'User(usr_id={self.usr_id}, name={self.name} weight={self.weight}'
