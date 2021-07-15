# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder: speck_weg File: models.py
#

from sqlalchemy.orm import declarative_base, relationship
from .tables import tpr_table, tpl_table, tex_table

Base = declarative_base()


class TrainingProgram(Base):
    # table definitions
    __table__ = tpr_table

    # orm definitions
    training_plans = relationship('TrainingPlan', back_populates='training_program')

    def __repr__(self):
        return f'TrainingProgram(tpr_id={self.tpr_id!r}, tpr_name={self.tpr_name!r})'


class TrainingPlan(Base):
    # table definitions
    __table__ = tpl_table

    # orm definitions
    training_program = relationship('TrainingProgram', back_populates='training_plans')

    def __repr__(self):
        return f'TrainingPlan(tpl_id={self.tpl_id!r}, tpl_name={self.tpl_name!r})'


class TrainingExcercise(Base):
    # table definitions
    __table__ = tex_table

    # orm definitions

    def __repr__(self):
        return f'TrainingExercise(tex_id={self.tex_id!r}, tex_name={self.tex_name!r})'