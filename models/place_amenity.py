#!/usr/bin/python
""" Place + Amenity models """

from datetime import datetime
import uuid
import re
from flask import jsonify, request, abort
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from data import storage, Base


# define the many-to-many table
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True)
)

class Place(Base):
    """Representation of place """

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
    can_init_list = ["city_id", "host_id", "name", "description", "number_rooms", "number_bathrooms", "max_guest", "price_by_night", "latitude", "longitude"]
    can_update_list = ["name", "description", "price", "max_guests"]

    # Class attrib defaults
    __tablename__ = 'places'
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    __city_id = Column("city_id", String(60), ForeignKey('cities.id'), nullable=False)
    __host_id = Column("host_id", String(60), ForeignKey('users.id'), nullable=False)
    __name = Column("name", String(128), nullable=False)
    __description = Column("description", String(1024), nullable=True)
    __address = Column("address", String(1024), nullable=True)
    __number_of_rooms = Column("number_of_rooms", Integer, nullable=False, default=0)
    __number_of_bathrooms = Column("number_of_bathrooms", Integer, nullable=False, default=0)
    __max_guests = Column("max_guests", Integer, nullable=False, default=0)
    __price_per_night = Column("price_per_night", Integer, nullable=False, default=0)
    __latitude = Column("latitude", Float, nullable=True)
    __longitude = Column("longitude", Float, nullable=True)
    amenities = relationship("Amenity", secondary=place_amenity, back_populates = 'places')
    reviews_r = relationship("Review", back_populates="place_r")
    owner_r = relationship("User", back_populates="properties_r")

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
    def city_id(self):
        """ Returns value of private property city_id """
        return self.__city_id

    @city_id.setter
    def city_id(self, value):
        """Setter for private prop city_id"""
        self.__city_id = value

    @property
    def host_id(self):
        """ Returns value of private property host_id """
        return self.__host_id

    @host_id.setter
    def host_id(self, value):
        """Setter for private prop host_id"""
        self.__host_id = value

    @property
    def name(self):
        """ Returns value of private property name """
        return self.__name

    @name.setter
    def name(self, value):
        """Setter for private prop name"""
        # Can't think of any special checks to perform here tbh
        self.__name = value

    @property
    def description(self):
        """ Returns value of private property description """
        return self.__description

    @description.setter
    def description(self, value):
        """Setter for private prop description"""
        # Can't think of any special checks to perform here tbh
        self.__description = value

    @property
    def address(self):
        """ Returns value of private property address """
        return self.__address

    @address.setter
    def address(self, value):
        """Setter for private prop address"""
        # Can't think of any special checks to perform here tbh
        self.__address = value

    @property
    def number_of_rooms(self):
        """ Returns value of private property number_of_rooms """
        return self.__number_of_rooms

    @number_of_rooms.setter
    def number_of_rooms(self, value):
        """Setter for private prop number_of_rooms"""
        if isinstance(value, int):
            self.__number_of_rooms = value
        else:
            raise ValueError("Invalid value specified for Number of Rooms: {}".format(value))

    @property
    def number_of_bathrooms(self):
        """ Returns value of private property number_of_bathrooms """
        return self.__number_of_bathrooms

    @number_of_bathrooms.setter
    def number_of_bathrooms(self, value):
        """Setter for private prop number_of_bathrooms"""
        if isinstance(value, int):
            self.__number_of_bathrooms = value
        else:
            raise ValueError("Invalid value specified for Number of Bathrooms: {}".format(value))

    @property
    def max_guests(self):
        """ Returns value of private property max_guests """
        return self.__max_guests

    @max_guests.setter
    def max_guests(self, value):
        """Setter for private prop max_guests"""
        if isinstance(value, int):
            self.__max_guests = value
        else:
            raise ValueError("Invalid value specified for Max Guests: {}".format(value))

    @property
    def price_per_night(self):
        """ Returns value of private property price_per_night """
        return self.__price_per_night

    @price_per_night.setter
    def price_per_night(self, value):
        """Setter for private prop price_per_night"""
        if isinstance(value, int):
            self.__price_per_night = value
        else:
            raise ValueError("Invalid value specified for Price per Night: {}".format(value))

    @property
    def latitude(self):
        """ Returns value of private property latitude """
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        """Setter for private prop latitude"""
        if isinstance(value, float):
            self.__latitude = value
        else:
            raise ValueError("Invalid value specified for Latitude: {}".format(value))

    @property
    def longitude(self):
        """ Returns value of private property longitude """
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        """Setter for private prop longitude"""
        if isinstance(value, float):
            self.__longitude = value
        else:
            raise ValueError("Invalid value specified for Longitude: {}".format(value))

    # --- Static methods ---
    @staticmethod
    def all(return_raw_result = False):
        """ Class method that returns all places data"""
        output = []

        try:
            result = storage.get('Place')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load places!"

        if return_raw_result:
            return result

        for row in result:
            # Note that we are using the amenities relationship to get the data we need
            place_amenity_ids = []
            for item in row.amenities:
                place_amenity_ids.append(item.id)

            output.append({
                "id": row.id,
                "name": row.name,
                "description": row.description,
                "address": row.address,
                "city_id": row.city_id,
                "latitude": row.latitude,
                "longitude": row.longitude,
                "host_id": row.host_id,
                "number_of_rooms": row.number_of_rooms,
                "number_of_bathrooms": row.number_of_bathrooms,
                "price_per_night": row.price_per_night,
                "max_guests": row.max_guests,
                "amenity_ids": place_amenity_ids,
                "created_at": row.created_at.strftime(Place.datetime_format),
                "updated_at": row.updated_at.strftime(Place.datetime_format)
            })

        return jsonify(output)

    @staticmethod
    def specific(place_id):
        """ Class method that returns a specific place's data"""
        try:
            result: Place = storage.get('Place', 'id', place_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Place data!"

        # there's only one item in result
        row = result[0]

        # Note that we are using the amenities relationship to get the data we need
        place_amenity_ids = []
        for item in row.amenities:
            place_amenity_ids.append(item.id)

        output = {
                "id": row.id,
                "name": row.name,
                "description": row.description,
                "address": row.address,
                "city_id": row.city_id,
                "latitude": row.latitude,
                "longitude": row.longitude,
                "host_id": row.host_id,
                "number_of_rooms": row.number_of_rooms,
                "number_of_bathrooms": row.number_of_bathrooms,
                "price_per_night": row.price_per_night,
                "max_guests": row.max_guests,
                "amenity_ids": place_amenity_ids,
                "created_at": row.created_at.strftime(Place.datetime_format),
                "updated_at": row.updated_at.strftime(Place.datetime_format)
        }

        return jsonify(output)

    @staticmethod
    def create():
        """ Class method that creates a new place"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        # Make sure everything we need is in the request payload
        for k in Place.can_init_list:
            if k not in data:
                abort(400, "Unable to create new Place! Missing attribute {}.".format(k))

        city_exists = storage.get('City', 'id', data["city_id"])
        if city_exists is None:
            abort(400, "Specified city does not exist")

        host_exists = storage.get('User', 'id', data["host_id"])
        if host_exists is None:
            abort(400, "Specified host does not exist")

        # Check whether the amenities all exist first
        if not storage.contains('Amenity', data['amenity_ids']):
            abort(400, "One or more specified Amenity ids do not exist!")

        # Use transactions here in case something goes wrong with the Place insert or the PlaceAmenity inserts
        try:
            # create object for the new Place
            new_place = Place(
                city_id=data["city_id"],
                host_id=data["host_id"],
                name=data["name"],
                description=data["description"],
                address=data["address"],
                number_of_rooms=data["number_of_rooms"],
                number_of_bathrooms=data["number_of_bathrooms"],
                max_guests=data["max_guests"],
                price_per_night=data["price_per_night"],
                latitude=data["latitude"],
                longitude=data["longitude"]
            )

            # Create the objects for the many-to-many records
            new_place_amenities = []
            for amenity_id in data['amenity_ids']:
                new_place_amenities.append(
                    PlaceAmenity(
                        place_id=new_place.id,
                        amenity_id=amenity_id,
                    )
                )
        except ValueError as exc:
            return repr(exc) + "\n"

        try:
            # Take note of the FALSE in the .add_all below so that it won't do a session commit
            # Let the .add for the new_place be the one that commits it all to the DB
            # All Or Nothing. I want to make sure everything gets in.
            storage.add_all(new_place_amenities, False)
            storage.add(new_place)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Place!"

        output = {
            "id": new_place.id,
            "city_id": new_place.city_id,
            "host_id": new_place.host_id,
            "name": new_place.name,
            "description": new_place.description,
            "address": new_place.address,
            "number_of_rooms": new_place.number_of_rooms,
            "number_of_bathrooms": new_place.number_of_bathrooms,
            "max_guests": new_place.max_guests,
            "price_per_night": new_place.price_per_night,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "created_at": new_place.created_at.strftime(Place.datetime_format),
            "updated_at": new_place.updated_at.strftime(Place.datetime_format)
        }

        return jsonify(output)

    @staticmethod
    def update(place_id):
        """ Class method that updates an existing place"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        try:
            # update the Place record.
            result = storage.update('Place', place_id, data, Place.can_update_list)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified place!"

        output = {
            "id": result.id,
            "city_id": result.city_id,
            "host_id": result.host_id,
            "name": result.name,
            "description": result.description,
            "address": result.address,
            "number_of_rooms": result.number_of_rooms,
            "number_of_bathrooms": result.number_of_bathrooms,
            "max_guests": result.max_guests,
            "price_per_night": result.price_per_night,
            "latitude": result.latitude,
            "longitude": result.longitude,
            "created_at": result.created_at.strftime(Place.datetime_format),
            "updated_at": result.updated_at.strftime(Place.datetime_format)
        }

        return jsonify(output)

    @staticmethod
    def amenities_data():
        """ grab the data from the many to many table """
        query_txt = """
            SELECT p.id AS place_id, p.name AS place_name, a.name AS amenity_name, a.id AS amenity_id
            FROM place_amenity pa 
            LEFT JOIN places p ON p.id = pa.place_id 
            LEFT JOIN amenities a ON a.id = pa.amenity_id 
            ORDER BY p.name ASC, a.name ASC
        """

        output = []
        result = storage.raw_sql(query_txt)
        for row in result:
            output.append({
                "place_id": row.place_id,
                "place_name": row.place_name,
                "amenity_name": row.amenity_name,
                "amenity_id": row.amenity_id
            })

        return output


class Amenity(Base):
    """Representation of amenity """

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
    can_init_list = ["name"]
    can_update_list = ["name"]

    # Class attrib defaults
    __tablename__ = 'amenities'
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    __name = Column("name", String(128), nullable=False)
    places = relationship("Place", secondary=place_amenity, back_populates = 'amenities')

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
            raise ValueError("Invalid amenity name specified: {}".format(value))

    # --- Static methods ---
    @staticmethod
    def all(return_raw_result=False):
        """ Class method that returns all amenities data"""
        output = []

        try:
            result = storage.get('Amenity')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load amenities!"

        if return_raw_result:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "name": row.name,
                "created_at": row.created_at.strftime(Amenity.datetime_format),
                "updated_at": row.updated_at.strftime(Amenity.datetime_format)
            })

        return jsonify(output)

    @staticmethod
    def specific(amenity_id):
        """ Class method that returns a specific amenity's data"""
        try:
            result: Amenity = storage.get('Amenity', 'id', amenity_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Amenity data!"

        output = {
            "id": result[0].id,
            "name": result[0].name,
            "created_at": result[0].created_at.strftime(Amenity.datetime_format),
            "updated_at": result[0].updated_at.strftime(Amenity.datetime_format)
        }

        return jsonify(output)

    @staticmethod
    def create():
        """ Class method that creates a new amenity"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()
        if 'name' not in data:
            abort(400, "Missing name")

        exists = storage.get('Amenity', '_Amenity__name', data["name"])
        if len(exists) > 0:
            abort(400, "Specified amenity already exists")

        try:
            new_amenity = Amenity(
                name=data["name"]
            )
        except ValueError as exc:
            return repr(exc) + "\n"

        try:
            storage.add(new_amenity)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Amenity!"

        output = {
            "id": new_amenity.id,
            "name": new_amenity.name,
            "created_at": new_amenity.created_at.strftime(Amenity.datetime_format),
            "updated_at": new_amenity.updated_at.strftime(Amenity.datetime_format)
        }

        return jsonify(output)

    @staticmethod
    def update(amenity_id):
        """ Class method that updates an existing amenity"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        try:
            # update the Amenity record. Only name can be changed
            result = storage.update('Amenity', amenity_id, data, Amenity.can_update_list)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified amenity!"

        output = {
            "id": result.id,
            "name": result.name,
            "country_id": result.country_id,
            "created_at": result.created_at.strftime(Amenity.datetime_format),
            "updated_at": result.updated_at.strftime(Amenity.datetime_format)
        }

        return jsonify(output)

    @staticmethod
    def create_place_relationship(data):
        """ This will create a many-to-many record to link a place with an amenity """

        # 1. check if the pairing exists or not
        query_txt = """
            SELECT * 
            FROM place_amenity pa 
            WHERE place_id = '""" + data['place'] + """' AND amenity_id = '""" + data['amenity'] + """'
        """

        result = storage.raw_sql(query_txt)

        count = 0
        for row in result:
            count += 1

        if count > 0:
            abort(400, "Specified pairing already exists")

        # 1. pairing does not exist, create the record
        insert_query_txt = """
            INSERT INTO place_amenity
            (place_id, amenity_id)
            VALUES('""" + data['place'] + """', '""" + data['amenity'] + """');
        """

        try:
            # If I don't do a session commit, the changes won't get written to the database
            # The changes will only exist in memory as long as the database session is active
            insert_result = storage.raw_sql(insert_query_txt, True)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add place-amenity pairing record!"

        return 'OK'
