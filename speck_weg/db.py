# fingertraining
# Stefan Hochuli, 14.07.2021,
# Folder: speck_weg File: db.py
#

from typing import List, Any, Type, Union, TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import metadata

if TYPE_CHECKING:
    from sqlalchemy import Column
    from sqlalchemy.orm import DeclarativeMeta


def start_session(drop_all=False):
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/speck_weg',
                           echo=True, future=True)
    # echo -> stdout, future -> sqlalchemy 2.0 style

    # Temporary drop for changes in tables and models
    if drop_all:
        metadata.drop_all(engine)

    metadata.create_all(engine)

    # Start the session
    session = Session(engine)
    return session


class CRUD:

    def __init__(self, s: 'Session' = None, drop_all=False):
        if s:
            self.session = s
        else:
            self.session = start_session(drop_all)

    def create(self, obj: Union[List, 'DeclarativeMeta']):

        try:
            if isinstance(obj, list):
                for o in obj:
                    self.session.add(o)
            else:
                self.session.add(obj)
            self.session.commit()
        except Exception as exc:
            print(exc)
            raise exc

    def read_first(self, cls: Type['DeclarativeMeta']) -> Any:

        stmt = select(cls)

        try:
            res = self.session.execute(stmt).scalars().first()
        except Exception as exc:
            print(exc)
            raise exc

        return res

    def read_all(self, cls: Type['DeclarativeMeta']) -> List[Any]:

        stmt = select(cls)

        # without scalars --> rows with lists of obj
        try:
            res = self.session.execute(stmt).scalars()
        except Exception as exc:
            print(exc)
            raise exc

        return res

    def read_stmt(self, stmt):
        try:
            res = self.session.execute(stmt).scalars()
        except Exception as exc:
            print(exc)
            raise exc

        return res

    def read(self, cls: Type['DeclarativeMeta'], column: 'Column', value: int):

        print('db_read')
        stmt = select(cls).where(column == value)

        try:
            res = self.session.execute(stmt).scalars()
        except Exception as exc:
            print(exc)
            raise exc

        return res

    def update(self):
        # commit recent changes
        self.session.commit()

    def delete(self, obj: Union[List, 'DeclarativeMeta']):

        try:
            if isinstance(obj, list):
                for o in obj:
                    self.session.delete(o)
            else:
                self.session.delete(obj)
            self.session.commit()

        except Exception as exc:
            print(exc)
            raise exc
