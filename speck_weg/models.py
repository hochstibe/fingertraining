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
        return f'TrainingProgram(tpr_id={self.tpr_id!r}, name={self.name!r})'


class TrainingPlan(Base):
    # table definitions
    __table__ = tpl_table

    # orm definitions
    training_program = relationship('TrainingProgram', back_populates='training_plans')
    training_exercises = relationship('TrainingExercise', back_populates='training_plan')

    def __repr__(self):
        return f'TrainingPlan(tpl_id={self.tpl_id!r}, name={self.name!r})'


class TrainingExercise(Base):
    # table definitions
    __table__ = tex_table

    # orm definitions
    training_plan = relationship('TrainingPlan', back_populates='training_exercises')

    def __repr__(self):
        return f'TrainingExercise(tex_id={self.tex_id!r}, name={self.name!r})'
