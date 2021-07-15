# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder: speck_weg File: db.py
#

from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@localhost:5432/speck_weg',
                       echo=True, future=True)  # echo -> stdout, future -> sqlalchemy 2.0 style
