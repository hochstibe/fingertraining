# fingertraining
# Stefan Hochuli, 09.09.2021,
# Folder: speck_weg/app File: training_theme.py
#

from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import select, update, bindparam

from ..models import TrainingThemeModel

if TYPE_CHECKING:
    from ..db import CRUD


class TrainingTheme:
    def __init__(self, db: 'CRUD',
                 tth_id: int = None, max_sequence: int = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.model: Optional['TrainingThemeModel'] = None

        if tth_id:
            stmt = select(TrainingThemeModel).where(TrainingThemeModel.tth_id == tth_id)
            res = self.db.read_one(stmt)
            self.model = res
        else:
            self.model = None
        self.max_sequence = max_sequence  # current maximum of existing training themes

    def add_theme(self, name: str, description: str):
        self.model = TrainingThemeModel(sequence=self.max_sequence+1)
        self.update_model(name, description)
        self.db.create(self.model)
        # Model saved -> clear for adding another one
        self.model = None
        self.max_sequence += 1  # if other themes are created

    def edit_theme(self, name: str, description: str):
        # updates all attributes (not the sequence, this is done from the collection)
        self.update_model(name, description)
        self.db.update()

    def update_model(self, name: str, description: str):
        self.model.name = name
        self.model.description = description


class TrainingThemeCollection:
    def __init__(self, db: 'CRUD',
                 model_list: List['TrainingThemeModel'] = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.model_list: List['TrainingThemeModel'] = []
        if model_list:
            self.model_list = model_list

    def read_themes(self):

        stmt = select(
            TrainingThemeModel).order_by(
            TrainingThemeModel.sequence).order_by(
            TrainingThemeModel.name)
        self.model_list = list(self.db.read_stmt(stmt))

    def update_sequence(self, tth_ids: List[int]):
        # stmt = update(TrainingThemeModel).where(
        #     TrainingThemeModel.tth_id == tth_id).values(sequence=i + 1)
        payload = [{'b_tth_id': tth_id, 'b_sequence': i+1} for i, tth_id in enumerate(tth_ids)]
        stmt = update(
            TrainingThemeModel).where(
            TrainingThemeModel.tth_id == bindparam('b_tth_id')).values(
            sequence=bindparam('b_sequence')
        )
        self.db.update(stmt, payload)
        self.read_themes()

    def remove_theme(self, tth_id: int = None):  # , row: int = None):
        if tth_id:
            ids = [tth.tth_id for tth in self.model_list]
            idx = ids.index(tth_id)
            print(tth_id, ids, idx)
            tth = self.model_list.pop(idx)
            self.db.delete(tth)

            # update the sequence for the remaining themes
            ids = [tth.tth_id for tth in self.model_list]
            if ids:
                self.update_sequence(ids)
