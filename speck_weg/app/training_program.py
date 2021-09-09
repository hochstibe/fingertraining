# fingertraining
# Stefan Hochuli, 09.09.2021,
# Folder: speck_weg/app File: training_program.py
#

from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import select, update, bindparam

from ..models import TrainingProgramModel

if TYPE_CHECKING:
    from ..db import CRUD


class TrainingProgram:
    def __init__(self, db: 'CRUD',
                 tpr_tth_id: int, tpr_id: int = None, max_sequence: int = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.model: Optional['TrainingProgramModel'] = None
        self.tpr_tth_id = tpr_tth_id  # parent training theme

        if tpr_id:
            stmt = select(TrainingProgramModel).where(TrainingProgramModel.tpr_id == tpr_id)
            res = self.db.read_one(stmt)
            self.model = res
        else:
            self.model = None
        self.max_sequence = max_sequence  # current maximum of existing training themes

    def add_program(self, name: str, description: str):
        self.model = TrainingProgramModel(tpr_tth_id=self.tpr_tth_id, sequence=self.max_sequence+1)
        self.update_model(name, description)
        self.db.create(self.model)
        # Model saved -> clear for adding another one
        self.model = None
        self.max_sequence += 1  # if other themes are created

    def edit_program(self, name: str, description: str):
        # updates all attributes (not the sequence, this is done from the collection)
        self.update_model(name, description)
        self.db.update()

    def update_model(self, name: str, description: str):
        self.model.name = name
        self.model.description = description


class TrainingProgramCollection:
    def __init__(self, db: 'CRUD',
                 model_list: List['TrainingProgramModel'] = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.model_list: List['TrainingProgramModel'] = []
        if model_list:
            self.model_list = model_list

    def read_programs(self, tth_id: int):

        stmt = select(
            TrainingProgramModel).where(
            TrainingProgramModel.tpr_tth_id == tth_id).order_by(
            TrainingProgramModel.sequence).order_by(
            TrainingProgramModel.name)
        self.model_list = list(self.db.read_stmt(stmt))

    def update_sequence(self, tpr_ids: List[int], tth_id: int):
        payload = [{'b_tpr_id': tpr_id, 'b_sequence': i+1} for i, tpr_id in enumerate(tpr_ids)]
        stmt = update(
            TrainingProgramModel).where(
            TrainingProgramModel.tpr_id == bindparam('b_tpr_id')).values(
            sequence=bindparam('b_sequence')
        )
        self.db.update(stmt, payload)
        self.read_programs(tth_id)

    def remove_program(self, tpr_id: int = None):
        if tpr_id:
            ids = [tpr.tpr_id for tpr in self.model_list]
            idx = ids.index(tpr_id)
            print(tpr_id, ids, idx)

            tpr = self.model_list.pop(idx)
            tth_id = tpr.tpr_tth_id
            self.db.delete(tpr)

            # update the sequence for the remaining programs
            ids = [tpr.tpr_id for tpr in self.model_list]
            if ids:
                self.update_sequence(ids, tth_id)
