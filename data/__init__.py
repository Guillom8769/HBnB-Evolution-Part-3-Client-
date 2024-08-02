#!/usr/bin/python3
""" initialize the storage used by models """

import os
from data.db_storage import DBStorage
from sqlalchemy.ext.declarative import declarative_base

# check for TESTING=1 from command line
# command to use: TESTING=1 python3 -m unittest discover
is_testing = "TESTING" in os.environ and os.environ['TESTING'] == "1"

# No more File Storage! We are only going to be using the DB for storage
Base = declarative_base()
storage = DBStorage(Base)
