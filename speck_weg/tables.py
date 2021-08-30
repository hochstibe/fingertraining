# fingertraining
# Stefan Hochuli, 14.07.2021,
# Folder: speck_weg File: tables.py
#

from sqlalchemy import (MetaData, Table, Column,
                        Integer, String, DateTime, Float,
                        ForeignKey, UniqueConstraint, text)
from sqlalchemy.sql import func

metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_N_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

tth_table = Table(
    'training_theme', metadata,
    Column('tth_id', Integer, primary_key=True, autoincrement='auto'),
    Column('name', String(63), nullable=False),
    Column('description', String(1023), nullable=True),
    Column('sequence', Integer, nullable=False),

    # Constraints
    UniqueConstraint('name'),
)

tpr_table = Table(
    'training_program', metadata,
    Column('tpr_id', Integer, primary_key=True, autoincrement='auto'),
    Column('tpr_tth_id', ForeignKey('training_theme.tth_id'), nullable=False),
    Column('name', String(63), nullable=False),
    Column('description', String(1023), nullable=True),
    Column('sequence', Integer, nullable=False),

    # Constraints
    UniqueConstraint('tpr_tth_id', 'name'),
)

tex_table = Table(
    'training_exercise', metadata,
    Column('tex_id', Integer, primary_key=True, autoincrement='auto'),
    # tex_usr_id is referenced, if the body weight is relevant
    Column('tex_usr_id', Integer, ForeignKey('user.usr_id'), nullable=True),
    Column('name', String(63), nullable=False),
    Column('description', String(1023), nullable=True),
    Column('baseline_repetitions', Integer, nullable=False),
    Column('baseline_weight', Float, nullable=True),
    Column('baseline_duration', Float, nullable=True),

    # Constraints
    # Multiple exercises with the same name possible (2x half crimp big)
)

tpr_tex_table = Table(
    'training_program_exercise', metadata,
    Column('tpe_tpr_id', ForeignKey('training_program.tpr_id'), primary_key=True, nullable=False),
    Column('tpe_tex_id', ForeignKey('training_exercise.tex_id'), primary_key=True, nullable=False),
    Column('sequence', Integer, nullable=False),
)

wse_table = Table(
    'workout_session', metadata,
    Column('wse_id', Integer, primary_key=True, autoincrement='auto'),
    Column('wse_tpr_id', ForeignKey('training_program.tpr_id')),
    Column('date', DateTime(timezone=True), nullable=False,
           server_default=func.current_timestamp()),
    Column('comment', String(1023), nullable=True),
)

wex_table = Table(
    'workout_exercise', metadata,
    Column('wex_id', Integer, primary_key=True, autoincrement='auto'),
    Column('wex_wse_id', ForeignKey('workout_session.wse_id')),
    Column('wex_tex_id', ForeignKey('training_exercise.tex_id')),
    Column('repetitions', Integer, nullable=False),
    Column('weight', Float, nullable=True),
    Column('duration', Integer, nullable=True),
    Column('comment', String(1023), nullable=True),
)

usr_table = Table(
    'user', metadata,
    Column('usr_id', Integer, primary_key=True, autoincrement='auto'),
    Column('name', String(255), nullable=False),
    Column('weight', Float, nullable=False),
)
