# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder: speck_weg File: db.py
#

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .tables import metadata

engine = create_engine('postgresql://postgres:postgres@localhost:5432/speck_weg',
                       echo=True, future=True)  # echo -> stdout, future -> sqlalchemy 2.0 style


# Temporary drop for changes in tables and models
# metadata.drop_all(engine)
metadata.create_all(engine)
session = Session(engine)
