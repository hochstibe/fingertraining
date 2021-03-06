# fingertraining
# Stefan Hochuli, 14.07.2021,
# Folder: speck_weg File: models.py
#

from sqlalchemy import (MetaData, Column,
                        Integer, String, DateTime, Float,
                        ForeignKey, UniqueConstraint,
                        select, case, cast)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import create_view


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


class TrainingThemeModel(Base):
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
    training_programs = relationship('TrainingProgramModel', back_populates='training_theme',
                                     order_by='asc(TrainingProgramModel.sequence), '
                                              'asc(TrainingProgramModel.name)')

    def __repr__(self):
        return f'TrainingThemeModel(' \
               f'tth_id={self.tth_id!r}, name={self.name!r})'


class TrainingProgramModel(Base):
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
    training_theme = relationship('TrainingThemeModel', back_populates='training_programs')
    training_exercises = relationship('TrainingProgramExerciseModel',
                                      back_populates='training_program',
                                      order_by='asc(TrainingProgramExerciseModel.sequence)')
    workout_sessions = relationship('WorkoutSessionModel', back_populates='training_program')

    def __repr__(self):
        return f'TrainingProgramModel(' \
               f'tpr_id={self.tpr_id!r}, name={self.name!r})'


class TrainingExerciseModel(Base):
    # table definitions
    __tablename__ = 'training_exercise'
    # No unique constraint: Multiple exercises with the same name possible (2x half crimp big)

    tex_id = Column(Integer, primary_key=True, autoincrement='auto')
    tex_usr_id = Column(Integer, ForeignKey('user.usr_id'), nullable=True)
    name = Column(String(63), nullable=False)
    description = Column(String(1023), nullable=True)
    baseline_sets = Column(Integer, nullable=False)
    baseline_repetitions = Column(Integer, nullable=False)
    baseline_custom_weight = Column(Float, nullable=True)
    baseline_duration = Column(Float, nullable=True)
    # Todo: Duration in seconds --> Int probably better than float

    # orm definitions
    training_programs = relationship('TrainingProgramExerciseModel',
                                     back_populates='training_exercise',
                                     cascade="all, delete")
    workout_exercises = relationship('WorkoutExerciseModel', back_populates='training_exercise')
    user = relationship('UserModel', back_populates='training_exercises')

    def __repr__(self):
        return f'TrainingExerciseModel(' \
               f'tex_id={self.tex_id!r}, name={self.name!r})'


class TrainingProgramExerciseModel(Base):
    # table definitions
    __tablename__ = 'training_program_exercise'
    # Todo: UniqueConstraint on the previous pk-columns (tpr_id, tex_id, sequence)?

    tpe_id = Column(Integer, primary_key=True, autoincrement='auto')
    tpe_tpr_id = Column(ForeignKey('training_program.tpr_id'), nullable=False)
    tpe_tex_id = Column(ForeignKey('training_exercise.tex_id'), nullable=False)
    sequence = Column(Integer, nullable=False)

    # orm definitions
    training_program = relationship('TrainingProgramModel', back_populates='training_exercises')
    training_exercise = relationship('TrainingExerciseModel', back_populates='training_programs')

    def __repr__(self):
        return f'TrainingProgramExerciseModel(tpe_id={self.tpe_id}, ' \
               f'tpe_tpr_id=({self.tpe_tpr_id!r}, tpe_tex_id={self.tpe_tex_id}, ' \
               f'sequence={self.sequence})'


class WorkoutSessionModel(Base):
    # table definitions
    __tablename__ = 'workout_session'

    wse_id = Column(Integer, primary_key=True, autoincrement='auto')
    wse_tpr_id = Column(ForeignKey('training_program.tpr_id'))
    date = Column(DateTime(timezone=True), nullable=False,
                  server_default=func.current_timestamp())
    comment = Column(String(1023), nullable=True)

    # orm definitions
    training_program = relationship('TrainingProgramModel', back_populates='workout_sessions')
    workout_exercises = relationship('WorkoutExerciseModel', back_populates='workout_session',
                                     order_by='asc(WorkoutExerciseModel.sequence), '
                                              'asc(WorkoutExerciseModel.set)')

    def __repr__(self):
        return f'WorkoutSessionModel(' \
               f'wse_id=({self.wse_id!r}, tse_tpr_id={self.wse_tpr_id}, date={self.date})'


class WorkoutExerciseModel(Base):
    # table definitions
    __tablename__ = 'workout_exercise'

    wex_id = Column(Integer, primary_key=True, autoincrement='auto')
    wex_wse_id = Column(ForeignKey('workout_session.wse_id'))
    wex_tex_id = Column(ForeignKey('training_exercise.tex_id'))
    sequence = Column(Integer, nullable=False)  # same sequence as in tpe for each exercise
    set = Column(Integer, nullable=False)
    repetitions = Column(Integer, nullable=False)
    weight = Column(Float, nullable=True)
    duration = Column(Float, nullable=True)
    comment = Column(String(1023), nullable=True)

    # orm definitions
    workout_session = relationship('WorkoutSessionModel', back_populates='workout_exercises')
    training_exercise = relationship('TrainingExerciseModel', back_populates='workout_exercises')

    def __repr__(self):
        return f'WorkoutExerciseModel(' \
               f'wex_id={self.wex_id}, wex_wse_id={self.wex_wse_id}, wex_tex_id={self.wex_tex_id})'


class UserModel(Base):
    # table definitions
    __tablename__ = 'user'

    usr_id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String(255), nullable=False)
    weight = Column(Float, nullable=False)

    training_exercises = relationship('TrainingExerciseModel', back_populates='user')

    def __repr__(self):
        return f'UserModel(usr_id={self.usr_id}, name={self.name} weight={self.weight}'


class TrainingExerciseView:
    # __view__ instead of __table

    __table__ = create_view(
        name='training_exercise_view',
        selectable=select(
            TrainingExerciseModel.tex_id.label('tex_id'),
            TrainingExerciseModel.name.label('name'),
            TrainingExerciseModel.description.label('description'),
            TrainingExerciseModel.baseline_sets.label('baseline_sets'),
            TrainingExerciseModel.baseline_repetitions.label('baseline_repetitions'),
            TrainingExerciseModel.baseline_duration.label('baseline_duration'),
            case(
                # is not None -> error
                (TrainingExerciseModel.baseline_custom_weight != None, TrainingExerciseModel.baseline_custom_weight),  # noqa
                (TrainingExerciseModel.tex_usr_id != None, UserModel.weight),  # noqa
                else_=None
            ).label('baseline_weight')
        ).outerjoin(TrainingExerciseModel.user),
        metadata=Base.metadata,
    )

    def __repr__(self):
        return f'TrainingExerciseView(tex_id={self.tex_id}, baseline_sets={self.baseline_sets}, baseline_weight={self.baseline_weight})'  # noqa


class WorkoutExerciseView(Base):
    _subq1 = select(
        WorkoutExerciseModel.wex_id, WorkoutExerciseModel.wex_wse_id,
        WorkoutExerciseModel.wex_tex_id, WorkoutExerciseModel.sequence, WorkoutExerciseModel.set,
        WorkoutExerciseModel.weight, WorkoutExerciseModel.duration,
        WorkoutExerciseModel.repetitions, WorkoutExerciseModel.comment,
        TrainingExerciseModel.name, TrainingExerciseModel.baseline_duration,
        TrainingExerciseModel.baseline_repetitions,
        case(
            (TrainingExerciseModel.baseline_custom_weight != None, TrainingExerciseModel.baseline_custom_weight),  # noqa
            (TrainingExerciseModel.tex_usr_id != None, UserModel.weight),  # noqa
            else_=None
        ).label('baseline_weight')
    ).select_from(WorkoutExerciseModel).outerjoin(
        WorkoutExerciseModel.training_exercise).outerjoin(
        TrainingExerciseModel.user
    ).subquery()
    _subq2 = select(
        _subq1.c.wex_id, _subq1.c.wex_wse_id, _subq1.c.wex_tex_id, _subq1.c.sequence, _subq1.c.set,
        _subq1.c.weight, _subq1.c.duration, _subq1.c.repetitions,
        _subq1.c.name,
        (cast(_subq1.c.repetitions, Float) / cast(_subq1.c.baseline_repetitions, Float)).label(
            'score_repetitions'),
        case(
            (_subq1.c.baseline_weight != None, _subq1.c.weight / _subq1.c.baseline_weight),  # noqa
            else_=1.0
        ).label('score_weight'),
        case(
            (_subq1.c.baseline_duration != None, _subq1.c.duration / _subq1.c.baseline_duration),  # noqa
            else_=1.0
        ).label('score_duration')
    ).subquery()
    __table__ = create_view(
        name='workout_exercise_view',
        selectable=select(
            _subq2.c.wex_id, _subq2.c.wex_wse_id, _subq2.c.wex_tex_id,
            _subq2.c.sequence, _subq2.c.set,
            _subq2.c.weight, _subq2.c.duration, _subq2.c.repetitions,  # all other attributes
            _subq2.c.name,
            (_subq2.c.score_repetitions * _subq2.c.score_weight * _subq2.c.score_duration).label(
                'score'),
        ).order_by(_subq2.c.wex_wse_id, _subq2.c.sequence, _subq2.c.set),
        metadata=Base.metadata
    )
