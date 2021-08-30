# fingertraining
# Stefan Hochuli, 14.07.2021,
# Folder: speck_weg File: models.py
#

from sqlalchemy import (MetaData, Column,
                        Integer, String, DateTime, Float,
                        ForeignKey, UniqueConstraint)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_N_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

Base = declarative_base(metadata=metadata)


class TrainingTheme(Base):
    # table definitions
    __tablename__ = 'training_theme'
    __table_args__ = (
        UniqueConstraint('name'),
    )

    tth_id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String(63), nullable=False)
    description = Column(String(1023), nullable=True)
    sequence = Column(Integer, nullable=False)

    # orm definitions
    training_programs = relationship('TrainingProgram', back_populates='training_theme',
                                     order_by='asc(TrainingProgram.sequence), '
                                              'asc(TrainingProgram.name)')

    def __repr__(self):
        return f'TrainingTheme(' \
               f'tth_id={self.tth_id!r}, name={self.name!r})'


class TrainingProgram(Base):
    # table definitions
    __tablename__ = 'training_program'
    __table_args__ = (
        UniqueConstraint('tpr_tth_id', 'name'),
    )

    tpr_id = Column(Integer, primary_key=True, autoincrement='auto')
    tpr_tth_id = Column(ForeignKey('training_theme.tth_id'), nullable=False)
    name = Column(String(63), nullable=False)
    description = Column(String(1023), nullable=True)
    sequence = Column(Integer, nullable=False)

    # orm definitions
    training_theme = relationship('TrainingTheme', back_populates='training_programs')
    training_exercises = relationship('TrainingProgramExercise', back_populates='training_program',
                                      order_by='asc(TrainingProgramExercise.sequence)')
    workout_sessions = relationship('WorkoutSession', back_populates='training_program')

    def __repr__(self):
        return f'TrainingProgram(' \
               f'tpr_id={self.tth_id!r}, name={self.name!r})'


class TrainingExercise(Base):
    # table definitions
    __tablename__ = 'training_exercise'
    # No unique constraint: Multiple exercises with the same name possible (2x half crimp big)

    tex_id = Column(Integer, primary_key=True, autoincrement='auto')
    # tex_usr_id is referenced, if the body weight is relevan
    tex_usr_id = Column(Integer, ForeignKey('user.usr_id'), nullable=True)
    name = Column(String(63), nullable=False)
    description = Column(String(1023), nullable=True)
    baseline_repetitions = Column(Integer, nullable=False)
    baseline_weight = Column(Float, nullable=True)
    baseline_duration = Column(Float, nullable=True)

    # orm definitions
    training_programs = relationship('TrainingProgramExercise', back_populates='training_exercise',
                                     cascade="all, delete")
    workout_exercises = relationship('WorkoutExercise', back_populates='training_exercise')

    def __repr__(self):
        return f'TrainingExercise(' \
               f'tex_id={self.tex_id!r}, name={self.name!r})'


class TrainingProgramExercise(Base):
    # table definitions
    __tablename__ = 'training_program_exercise'

    tpe_tpr_id = Column(ForeignKey('training_program.tpr_id'), primary_key=True, nullable=False)
    tpe_tex_id = Column(ForeignKey('training_exercise.tex_id'), primary_key=True, nullable=False)
    sequence = Column(Integer, nullable=False)

    # orm definitions
    training_program = relationship('TrainingProgram', back_populates='training_exercises')
    training_exercise = relationship('TrainingExercise', back_populates='training_programs',)

    def __repr__(self):
        return f'TrainingProgramExercise(wse_tpe_tpr_id=({self.tpe_tpr_id!r}, ' \
               f'tpe_tex_id={self.tpe_tex_id}, sequence={self.sequence})'


class WorkoutSession(Base):
    # table definitions
    __tablename__ = 'workout_session'

    wse_id = Column(Integer, primary_key=True, autoincrement='auto')
    wse_tpr_id = Column(ForeignKey('training_program.tpr_id'))
    date = Column(DateTime(timezone=True), nullable=False,
                  server_default=func.current_timestamp())
    comment = Column(String(1023), nullable=True)

    # orm definitions
    training_program = relationship('TrainingProgram', back_populates='workout_sessions')
    workout_exercises = relationship('WorkoutExercise', back_populates='workout_session')

    def __repr__(self):
        return f'WorkoutSession(' \
               f'wse_id=({self.wse_id!r}, tse_tpr_id={self.wse_tpr_id}, date={self.date})'


class WorkoutExercise(Base):
    # table definitions
    __tablename__ = 'workout_exercise'

    wex_id = Column(Integer, primary_key=True, autoincrement='auto')
    wex_wse_id = Column(ForeignKey('workout_session.wse_id'))
    wex_tex_id = Column(ForeignKey('training_exercise.tex_id'))
    repetitions = Column(Integer, nullable=False)
    weight = Column(Float, nullable=True)
    duration = Column(Integer, nullable=True)
    comment = Column(String(1023), nullable=True)

    # orm definitions
    workout_session = relationship('WorkoutSession', back_populates='workout_exercises')
    training_exercise = relationship('TrainingExercise', back_populates='workout_exercises')

    def __repr__(self):
        return f'WorkoutExercise(' \
               f'wex_id={self.wex_id}, wex_wse_id={self.wex_wse_id}, wex_tex_id={self.wex_tex_id})'


class User(Base):
    # table definitions
    __tablename__ = 'user'

    usr_id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String(255), nullable=False)
    weight = Column(Float, nullable=False)

    def __repr__(self):
        return f'User(usr_id={self.usr_id}, name={self.name} weight={self.weight}'
