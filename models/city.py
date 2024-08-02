#!/usr/bin/python
""" City model """

from datetime import datetime
import uuid
import re
from flask import jsonify, request, abort
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from data import storage, Base

class City(Base):
    """Representation of city """

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
    can_init_list = ["country_id", "name"]
    can_update_list = ["name"]

    # Class attrib defaults
    __tablename__ = 'cities'
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    __name = Column("name", String(128), nullable=False)
    __country_id = Column("country_id", String(128), ForeignKey('countries.id'), nullable=False)
    country = relationship("Country", back_populates="cities")

    # constructor
    def __init__(self, *args, **kwargs):
        """ constructor """
        # Set object instance defaults
        self.id = str(uuid.uuid4())

        # Note that setattr will call the setters for attribs in the list
        if kwargs:
            for key, value in kwargs.items():
                if key in self.can_init_list:
                    setattr(self, key, value)

    @property
    def name(self):
        """Getter for private prop name"""
        return self.__name

    @name.setter
    def name(self, value):
        """Setter for private prop name"""

        # ensure that the value is not spaces-only and is alphabets + spaces only
        is_valid_name = len(value.strip()) > 0 and re.search("^[a-zA-Z ]+$", value)
        if is_valid_name:
            self.__name = value
        else:
            raise ValueError("Invalid city name specified: {}".format(value))

    @property
    def country_id(self):
        """Getter for private prop country_id"""
        return self.__country_id

    @country_id.setter
    def country_id(self, value):
        """Setter for private prop country_id"""
        self.__country_id = value

    # --- Static methods ---
    @staticmethod
    def all(return_raw_result = False):
        """ Class method that returns all cities data"""
        output = []

        try:
            result = storage.get('City')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load cities!"

        if return_raw_result:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "name": row.name,
                "country_id": row.country_id,
                "created_at": row.created_at.strftime(City.datetime_format),
                "updated_at": row.updated_at.strftime(City.datetime_format)
            })

        return jsonify(output)

    @staticmethod
    def specific(city_id):
        """ Class method that returns a specific city's data"""
        try:
            result: City = storage.get('City', 'id', city_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load City data!"

        output = {
            "id": result[0].id,
            "name": result[0].name,
            "code": result[0].code,
            "created_at": result[0].created_at.strftime(City.datetime_format),
            "updated_at": result[0].updated_at.strftime(City.datetime_format)
        }

        return jsonify(output)

    @staticmethod
    def create():
        """ Class method that creates a new city"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()
        if 'name' not in data:
            abort(400, "Missing name")
        if 'country_id' not in data:
            abort(400, "Missing country id")

        exists = storage.get('Country', 'id', data["country_id"])
        if exists is None:
            abort(400, "Specified country does not exist")

        try:
            new_city = City(
                name=data["name"],
                country_id=data["country_id"]
            )
        except ValueError as exc:
            return repr(exc) + "\n"

        try:
            storage.add(new_city)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new City!"

        output = {
            "id": new_city.id,
            "name": new_city.name,
            "country_id": new_city.country_id,
            "created_at": new_city.created_at.strftime(City.datetime_format),
            "updated_at": new_city.updated_at.strftime(City.datetime_format)
        }

        return jsonify(output)

    @staticmethod
    def update(city_id):
        """ Class method that updates an existing city"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        try:
            # update the City record. Only name can be changed
            result = storage.update('City', city_id, data, City.can_update_list)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified city!"

        output = {
            "id": result.id,
            "name": result.name,
            "country_id": result.country_id,
            "created_at": result.created_at.strftime(City.datetime_format),
            "updated_at": result.updated_at.strftime(City.datetime_format)
        }

        return jsonify(output)
