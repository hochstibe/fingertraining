# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder:  File: main.py
#

from speck_weg.db import engine
from speck_weg.tables import metadata

metadata.create_all(engine)
