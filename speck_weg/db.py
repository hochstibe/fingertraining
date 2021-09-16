# fingertraining
# Stefan Hochuli, 14.07.2021,
# Folder: speck_weg File: db.py
#

from typing import List, Any, Type, Union, TYPE_CHECKING

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import sqlalchemy.exc

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

    try:
        metadata.create_all(engine, checkfirst=True)
    except(sqlalchemy.exc.OperationalError, sqlalchemy.exc.ProgrammingError):
        # if the view already exist -> only check tables
        for table in metadata.tables:
            metadata.tables[table].create(bind=engine, checkfirst=True)

    # Start the session
    # Todo: sessionmaker -> new session for new transactions or new session for new window
    # https://docs.sqlalchemy.org/en/14/orm/session_basics.html
    # scoped_session -> otherwise the objects are not within the separate sessions
    # https://docs.sqlalchemy.org/en/14/orm/session_basics.html#session-faq-whentocreate
    # --> now it is a session for everything (committing frequently)
    # --> they suggest opening a session for a user-interaction
    # --> control the session opening /closing in the app-scripts
    # one session: read 1000 the same object -> 0.6s
    # sessionmaker: read 1000 in new sessions -> 0.5s
    # for the application: now the objects are read once and then passed to windows
    # if individual sessions -> maybe query again for the object before e.g. change it

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
                self.session.add_all(obj)
            else:
                self.session.add(obj)
            self.session.commit()
        except Exception as exc:
            print(exc)
            raise exc

    def read_first(self, stmt) -> Any:

        try:
            res = self.session.execute(stmt).scalars().first()
        except Exception as exc:
            print(exc)
            raise exc

        return res

    def read_one(self, stmt, unique=False) -> Any:
        # error, if it cant find the tuple
        try:
            if unique:
                res = self.session.execute(stmt).scalars().unique().one()
            else:
                res = self.session.execute(stmt).scalars().one()
        except Exception as exc:
            print(exc)
            raise exc

        return res

    def read_all(self, cls: Type['DeclarativeMeta']) -> List[Any]:

        stmt = select(cls)

        # without scalars --> rows with lists of obj
        try:
            res = list(self.session.execute(stmt).scalars())
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

    def update(self, stmt=None, payload=None):
        # commit recent changes
        if stmt is not None:
            self.session.execute(stmt, payload)
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
