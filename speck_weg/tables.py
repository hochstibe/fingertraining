# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder: speck_weg File: tables.py
#

from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, UniqueConstraint

metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_N_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

tpr_table = Table(
    'training_program', metadata,
    Column('tpr_id', Integer, primary_key=True, autoincrement='auto'),
    Column('tpr_name', String(63), nullable=False),
    Column('tpr_description', String(1023), nullable=True),

    # Constraints
    UniqueConstraint('tpr_name')
)

tpl_table = Table(
    'training_plan', metadata,
    Column('tpl_id', Integer, primary_key=True, autoincrement='auto'),
    Column('tpl_name', String(63), nullable=False),
    Column('tpl_description', String(1023), nullable=True),
    Column('tpl_tpr_id', ForeignKey('training_program.tpr_id'), nullable=False)
    # Todo: Unique constraint tpl_name + tpl_tpr_id
)

tex_table = Table(
    'training_exercise', metadata,
    Column('tex_id', Integer, primary_key=True, autoincrement='auto'),
    Column('tex_name', String(63), nullable=False),
    Column('tex_description', String(1023), nullable=True),
    Column('tex_sequence', Integer, nullable=True),
    Column('tex_tpl_id', ForeignKey('training_plan.tpl_id'))
    # Todo: Unique constraint tex_name + tex_tpl_id
)

