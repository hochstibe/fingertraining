# fingertraining
# Stefan Hochuli, 09.09.2021,
# Folder: speck_weg/app File: user.py
#

from typing import Optional, Union, TYPE_CHECKING

from sqlalchemy import select

from speck_weg.models import UserModel

if TYPE_CHECKING:
    from ..db import CRUD


class User:
    def __init__(self, db: 'CRUD',
                 usr_id: int = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.model: Optional['UserModel'] = None

        # initially search for the current user (if not given)
        if usr_id:
            stmt = select(UserModel).where(UserModel.usr_id == usr_id)
            res = self.db.read_one(stmt)
            self.model = res
        else:
            self.model = None
        if not usr_id:
            self.model = self.read_current_user()

    def read_current_user(self) -> Union['UserModel', None]:
        # selects the first entry in the user table
        stmt = select(UserModel)
        return self.db.read_first(stmt)

    def update_usr_attributes(self, name: str, weight: float):
        # update all attributes

        self.model.name = name
        self.model.weight = weight

    def save_user(self, name: str, weight: float):
        if self.model:
            self.update_usr_attributes(name, weight)
            self.db.update()

        else:
            self.model = UserModel()
            self.update_usr_attributes(name, weight)
            self.db.create(self.model)
