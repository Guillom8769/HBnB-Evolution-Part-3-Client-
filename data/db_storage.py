#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb evolution"""

import importlib
from os import getenv
from copy import deepcopy
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

class DBStorage:
    """ Class for reading data from databases """
    __engine = None
    __session = None
    __module_names = {
        "User": "user",
        "Country": "country",
        "City": "city",
        "Amenity": "place_amenity",
        "Place": "place_amenity",
        "Review": "review"
    }

    def __init__(self, Base):
        """Instantiate a DBStorage object"""

        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        is_testing = getenv('TESTING')

        # If you were lazy and didn't specify anything on the command line, then the defaults below will be used
        # PLEASE DON'T DO THIS IN A REAL WORKING ENVIRONMENT
        if user is None:
            user = "hbnb_evo"
        if pwd is None:
            pwd = "hbnb_evo_pwd"
        if host is None:
            if getenv('IS_DOCKER_CONTAINER'):
                # make sure this is the same as the db container name in the docker compose file
                host = "hbnb_evo_2_db"
            else:
                host = "localhost"
        if db is None:
            if is_testing == "1":
                db = "hbnb_test_db"
            else:
                db = "hbnb_evo_db"

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db))

        if is_testing == "1":
            Base.metadata.drop_all(self.__engine)

        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def get(self, class_name="", key="", value=""):
        """ Return data for specified class name with or without record id"""

        if class_name == "":
            raise IndexError("Unable to load Model data. No class name specified")

        if class_name not in self.__module_names:
            raise IndexError("Unable to load Model data. Specified class name not found")

        namespace = self.__module_names[class_name]
        module = importlib.import_module("models." + namespace)
        class_ = getattr(module, class_name)

        if key != "" and value != "":
            try:
                rows = self.__session.query(class_).filter(getattr(class_, key) == value).all()
            except AttributeError:
                raise IndexError("Unable to load Model data. Attribute " + key + " not found")
        else:
            rows = self.__session.query(class_).all()

        return rows

    def add(self, new_record, do_commit=True):
        """ Adds another record to specified class """

        self.__session.add(new_record)

        if do_commit:
            self.__session.commit()
            self.__session.refresh(new_record)

    def add_all(self, new_records, do_commit=True):
        """ add and commit multiple records """

        self.__session.add_all(new_records)

        if do_commit:
            self.__session.commit()

    def update(self, class_name, record_id, update_data, allowed=None):
        """ Updates existing record of specified class """

        if class_name.strip() == "" or class_name not in self.__module_names:
            raise IndexError("Specified class name is not valid")

        namespace = self.__module_names[class_name]
        module = importlib.import_module("models." + namespace)
        class_ = getattr(module, class_name)

        try:
            record = self.__session.query(class_).filter(class_.id == record_id).limit(1).one()
        except Exception:
            raise IndexError("Unable to find the record to update")

        try:
            for k, v in update_data.items():
                if allowed is not None and len(allowed) > 0:
                    if k in allowed:
                        setattr(record, k, v)
                else:
                    setattr(record, k, v)

            record.updated_at = datetime.now()

            self.__session.commit()
        except Exception:
            raise IndexError("Unable to update record")

        return deepcopy(record)

    def contains(self, class_name, ids_list):
        """ Returns a simple TRUE or FALSE depending on whether all the ids in ids_list exist within the specified table """

        if class_name not in self.__module_names:
            raise IndexError("Unable to load Model data. Specified class name not found")

        if not ids_list:
            raise IndexError("No record ids specified.")

        namespace = self.__module_names[class_name]
        module = importlib.import_module("models." + namespace)
        class_ = getattr(module, class_name)

        rows = self.__session.query(class_).filter(
            getattr(class_, 'id').in_(ids_list)
        ).all()

        return len(rows) == len(ids_list)

    def raw_sql(self, query_txt, commit=False):
        """ The absolutely worst possible way to access the database using an ORM """
        sql = text(query_txt)
        result = self.__session.execute(sql)

        if commit:
            self.__session.commit()

        return result
