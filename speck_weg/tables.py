# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder: speck_weg File: tables.py
#

from sqlalchemy import (MetaData, Table, Column,
                        Integer, String, DateTime, Float,
                        ForeignKey, UniqueConstraint)
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

    # Constraints
    UniqueConstraint('name'),
)

tpr_table = Table(
    'training_program', metadata,
    Column('tpr_id', Integer, primary_key=True, autoincrement='auto'),
    Column('tpr_tth_id', ForeignKey('training_theme.tth_id'), nullable=False),
    Column('name', String(63), nullable=False),
    Column('description', String(1023), nullable=True),
    # Todo: Unique constraint tpl_name + tpl_tpr_id
)

tex_table = Table(
    'training_exercise', metadata,
    Column('tex_id', Integer, primary_key=True, autoincrement='auto'),
    Column('tex_tpr_id', ForeignKey('training_program.tpr_id')),
    Column('name', String(63), nullable=False),
    Column('description', String(1023), nullable=True),
    Column('sequence', Integer, nullable=True),
    # Todo: Unique constraint tex_name + tex_tpl_id
)

wse_table = Table(
    'workout_session', metadata,
    Column('wse_id', Integer, primary_key=True, autoincrement='auto'),
    Column('wse_tpr_id', ForeignKey('training_program.tpr_id')),
    Column('date', DateTime(timezone=True), nullable=False, server_default=func.current_timestamp()),
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
    Column('rate', Float, nullable=False),
)
