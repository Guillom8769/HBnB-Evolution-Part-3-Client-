#!/usr/bin/python
""" Country model """

from datetime import datetime
import uuid
import re
from copy import deepcopy
from flask import jsonify, request, abort
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from data import storage, Base
from models.city import City

class Country(Base):
    """Representation of country """

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
    can_init_list = ["name", "code"]
    can_update_list = ["name"]

    # Class attrib defaults
    __tablename__ = 'countries'
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    __name = Column("name", String(128), nullable=False)
    __code = Column("code", String(2), nullable=False)
    cities = relationship("City", back_populates="country", cascade="delete, delete-orphan")

    # Constructor
    def __init__(self, *args, **kwargs):
        """ constructor """
        # Set object instance defaults
        self.id = str(uuid.uuid4())

        # Note that setattr will call the setters for attribs in the list
        if kwargs:
            for key, value in kwargs.items():
                if key in self.can_init_list:
                    setattr(self, key, value)

    # --- Getters and Setters ---
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
            raise ValueError("Invalid country name specified: {}".format(value))

    @property
    def code(self):
        """Getter for private prop code"""
        return self.__code

    @code.setter
    def code(self, value):
        """Setter for private prop code"""

        # ensure that the value is not spaces-only and is two uppercase alphabets only
        is_valid_code = len(value.strip()) > 0 and re.search("^[A-Z][A-Z]$", value)
        if is_valid_code:
            self.__code = value
        else:
            raise ValueError("Invalid country code specified: {}".format(value))

    # --- Static methods ---
    @staticmethod
    def all(return_raw_result = False):
        """ Class method that returns all countries data"""
        output = []

        try:
            result = storage.get('Country')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load countries!"

        if return_raw_result:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "name": row.name,
                "code": row.code,
                "created_at": row.created_at.strftime(Country.datetime_format),
                "updated_at": row.updated_at.strftime(Country.datetime_format)
            })

        return jsonify(output)

    @staticmethod
    def specific(country_code):
        """ Class method that returns a specific country's data"""
        try:
            result: Country = storage.get('Country', '_Country__code', country_code)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Country data!"

        output = {
            "id": result[0].id,
            "name": result[0].name,
            "code": result[0].code,
            "created_at": result[0].created_at.strftime(Country.datetime_format),
            "updated_at": result[0].updated_at.strftime(Country.datetime_format)
        }

        return jsonify(output)

    @staticmethod
    def create():
        """ Class method that creates a new country"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()
        if 'name' not in data:
            abort(400, "Missing name")
        if 'code' not in data:
            abort(400, "Missing country code")

        exists = storage.get('Country', '_Country__code', data["code"])
        if len(exists) > 0:
            return "New country's code is the same as that of an existing country!"

        try:
            new_country = Country(
                name=data["name"],
                code=data["code"]
            )
        except ValueError as exc:
            return repr(exc) + "\n"

        try:
            storage.add(new_country)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Country!"

        output = {
            "id": new_country.id,
            "name": new_country.name,
            "code": new_country.code,
            "created_at": new_country.created_at.strftime(Country.datetime_format),
            "updated_at": new_country.updated_at.strftime(Country.datetime_format)
        }

        return jsonify(output)

    @staticmethod
    def create_from_form_submit(data):
        """ accepts form submit data to create new country """

        if 'name' not in data:
            abort(400, "Missing name")
        if 'code' not in data:
            abort(400, "Missing country code")

        exists = storage.get('Country', '_Country__code', data["code"])
        if len(exists) > 0:
            return "New country's code is the same as that of an existing country!"

        try:
            new_country = Country(
                name=data["name"],
                code=data["code"]
            )
        except ValueError as exc:
            return repr(exc) + "\n"

        try:
            storage.add(new_country)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Country!"

        return 'OK'

    @staticmethod
    def update(country_code):
        """ Class method that updates an existing country"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        country_data: Country = storage.get('Country', '_Country__code', country_code)
        if country_data is None:
            abort(400, "Country not found for code {}".format(country_code))

        try:
            # update the Country record. Only name can be changed
            result = storage.update('Country', country_data.id, data, Country.can_update_list)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified country!"

        output = {
            "id": result.id,
            "name": result.name,
            "code": result.code,
            "created_at": result.created_at.strftime(Country.datetime_format),
            "updated_at": result.updated_at.strftime(Country.datetime_format)
        }

        return jsonify(output)

    @staticmethod
    def cities_data(country_code):
        """ Class method that returns a specific country's cities"""
        # Unused at the moment.
        # This method can be replaced partially by the cities relationship defined above

        output = []

        # If the column is mapped to a private variable, the attr name is mangled like below
        try:
            country_data: Country = storage.get('Country', '_Country__code', country_code)
            result: City = storage.get('City', '_City__country_id', country_data[0].id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Country data!"

        for row in result:
            output.append({
                "id": row.id,
                "name": row.name,
                "country_id": row.country_id,
                "created_at":row.created_at.strftime(Country.datetime_format),
                "updated_at":row.updated_at.strftime(Country.datetime_format)
            })

        return jsonify(output)

    @staticmethod
    def places(country_code = "", amenities = ""):
        """ The big one! Everything we need is in here! """

        # --- Full SQL query Example ---
        # Run the individual subqueries to understand the results given by them.

        # SELECT id AS place_id, country_name, city_name, host_id, name, description, address, number_of_rooms, number_of_bathrooms, max_guests, price_per_night, latitude, longitude, GROUP_CONCAT(amenity_name)
        # FROM (
        #         SELECT co.name AS country_name, ci.name AS city_name, pl.*, am.name AS amenity_name
        #         FROM countries co
        #         LEFT JOIN cities ci ON co.id = ci.country_id
        #         LEFT JOIN places pl ON ci.id = pl.city_id
        #         LEFT JOIN place_amenity pa ON pl.id = pa.place_id
        #         LEFT JOIN amenities am on pa.amenity_id = am.id
        #         WHERE pl.id IN (
        #                 SELECT DISTINCT(place_id) FROM
        #                 (
        #                         SELECT place_id, count(amenity_id) AS amenity_count
        #                         FROM place_amenity
        #                         WHERE amenity_id IN ('036bc824-74ed-44dc-a183-1ab6c4878fc2', '2ec8cf22-e5ea-4a1f-aedd-89f15fcc60e9')
        #                         GROUP BY place_id
        #                 ) y
        #                 WHERE amenity_count = 2
        #         ) AND co.code = 'MY'
        # ) x
        # GROUP BY country_name, city_name, id

        # Note that the WHERE clause in the subquery may be different depending on what was selected in the form
        # Let's assemble the subquery first

        output = {}

        where_and = " WHERE "
        query_txt = "SELECT co.name AS country_name, ci.name AS city_name, pl.*, am.name as amenity_name \
            FROM countries co \
            LEFT JOIN cities ci ON co.id = ci.country_id \
            LEFT JOIN places pl ON ci.id = pl.city_id \
            LEFT JOIN place_amenity pa ON pl.id = pa.place_id \
            LEFT JOIN amenities am on pa.amenity_id = am.id "

        # If specific amenities were selected
        if amenities != "" and len(amenities) > 0:
            # Assemble the comma-separated list
            # 1. wrap each item in the list with inverted commas
            amenity_count = 0
            amenities_list = []
            for a in amenities:
                amenities_list.append("'" + a + "'")
                amenity_count = amenity_count + 1

            # 2. then turn it ionto a comma separated string
            amenities_comma_list = ",".join(amenities_list)

            query_txt = query_txt + "WHERE pl.id IN ( \
                    SELECT DISTINCT(place_id) FROM ( \
                        SELECT place_id, count(amenity_id) AS amenity_count \
                        FROM place_amenity \
                        WHERE amenity_id IN (" + amenities_comma_list + ") \
                        GROUP BY place_id \
                    ) y \
                    WHERE amenity_count = " + str(amenity_count) + " \
                )"
            where_and = " AND "

        # If a specific country was selected
        if country_code != "":
            query_txt = query_txt + where_and + "co.code = '" + country_code + "'"

        # Subquery complete!
        # Now, let's wrap it in the bigger GROUP BY query
        # Note that the subquery is given an alias. This is required
        query_txt = "SELECT id AS place_id, country_name, city_name, host_id, \
            name, description, address, number_of_rooms, number_of_bathrooms, \
            max_guests, price_per_night, latitude, longitude, \
            GROUP_CONCAT(amenity_name) as amenities \
            FROM (" + query_txt + ") x GROUP BY country_name, city_name, id"

        # This should give condense the results with the same country + city + place id
        # Amenities names will be squashed using GROUP_CONCAT into a comma separated string

        result = storage.raw_sql(query_txt)
        for row in result:
            if row.place_id:
                # let's start grouping by country code
                if row.country_name not in output:
                    output[row.country_name] = {}

                if row.city_name not in output[row.country_name]:
                    output[row.country_name][row.city_name] = []

                if row.city_name is not None:
                    amenities_array = []
                    if row.amenities:
                        amenities_array = row.amenities.split(",")

                    output[row.country_name][row.city_name].append({
                        "city_name": row.city_name,
                        "place_id": row.place_id,
                        "name": row.name,
                        "description": row.description,
                        "address": row.address,
                        "number_of_rooms": row.number_of_rooms,
                        "number_of_bathrooms": row.number_of_bathrooms,
                        "max_guests": row.max_guests,
                        "price_per_night": row.price_per_night,
                        "latitude": row.latitude,
                        "longitude": row.longitude,
                        "host_id": row.host_id,
                        "amenities": amenities_array
                    })

        return output
