# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder: speck_weg File: models.py
#

from sqlalchemy.orm import declarative_base, relationship
from .tables import tth_table, tpr_table, tex_table

Base = declarative_base()


class TrainingTheme(Base):
    # table definitions
    __table__ = tth_table

    # orm definitions
    training_programs = relationship('TrainingProgram', back_populates='training_theme')

    def __repr__(self):
        return f'TrainingTheme(tth_id={self.tth_id!r}, name={self.name!r})'


class TrainingProgram(Base):
    # table definitions
    __table__ = tpr_table

    # orm definitions
    training_theme = relationship('TrainingTheme', back_populates='training_programs')
    training_exercises = relationship('TrainingExercise', back_populates='training_program')

    def __repr__(self):
        return f'TrainingProgram(tpr_id={self.tth_id!r}, name={self.name!r})'


class TrainingExercise(Base):
    # table definitions
    __table__ = tex_table

    # orm definitions
    training_program = relationship('TrainingProgram', back_populates='training_exercises')

    def __repr__(self):
        return f'TrainingExercise(tex_id={self.tex_id!r}, name={self.name!r})'
