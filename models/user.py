#!/usr/bin/python
""" User model """

from datetime import datetime
import uuid
import re
from flask import jsonify, request, abort
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from data import storage, Base

class User(Base):
    """Representation of user """

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
    can_init_list = ["first_name", "last_name", "email", "password"]
    can_update_list = ["first_name", "last_name"]

    # Class attrib defaults
    __tablename__ = 'users'
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    __first_name = Column("first_name", String(128), nullable=True, default="")
    __last_name = Column("last_name", String(128), nullable=True, default="")
    __email = Column("email", String(128), nullable=False)
    __password = Column("password", String(128), nullable=False)
    reviews_r = relationship("Review", back_populates="user_r", cascade="delete, delete-orphan")
    properties_r = relationship("Place", back_populates="owner_r", cascade="delete, delete-orphan")

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
    def first_name(self):
        """Getter for private prop first_name"""
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        """Setter for private prop first_name"""

        # ensure that the value is alphabets only
        # Note that this won't allow names like Obi-wan or Al'azif
        is_valid_name = len(value.strip()) > 0 and re.search("^[a-zA-Z]+$", value)
        if is_valid_name:
            self.__first_name = value
        else:
            raise ValueError("Invalid first name specified: {}".format(value))

    @property
    def last_name(self):
        """Getter for private prop last_name"""
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        """Setter for private prop last_name"""

        # ensure that the value is alphabets only
        # Note that this won't allow names like Obi-wan or Al'azif
        is_valid_name = len(value.strip()) > 0 and re.search("^[a-zA-Z]+$", value)
        if is_valid_name:
            self.__last_name = value
        else:
            raise ValueError("Invalid last name specified: {}".format(value))

    @property
    def email(self):
        """Getter for private prop email"""
        return self.__email

    @email.setter
    def email(self, value):
        """Setter for private prop last_name"""

        # add a simple regex check for email format. Nothing too fancy.
        is_valid_email = len(value.strip()) > 0 and re.search("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", value)
        if is_valid_email:
            self.__email = value
        else:
            raise ValueError("Invalid email specified: {}".format(value))

    @property
    def password(self):
        """Getter for private prop email"""
        return self.__password

    @password.setter
    def password(self, value):
        """Setter for private prop email"""
        is_valid_password = len(value) >= 6
        if is_valid_password:
            self.__password = value
        else:
            raise ValueError("Password is too short! Min 6 characters required.")

    # --- Static methods ---
    @staticmethod
    def all(return_raw_result = False):
        """ Class method that returns all users data"""
        output = []

        try:
            result = storage.get('User')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load users!"

        if return_raw_result:
            return result

        for row in result:
            # use print(row.__dict__) to see the contents of the sqlalchemy model objects
            output.append({
                "id": row.id,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "email": row.email,
                "password": row.password,
                "created_at": row.created_at.strftime(User.datetime_format),
                "updated_at": row.updated_at.strftime(User.datetime_format)
            })

        return jsonify(output)

    @staticmethod
    def specific(user_id):
        """ Class method that returns a specific user's data"""
        output = []

        try:
            result: User = storage.get('User', 'id', user_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "User not found!"

        output.append({
            "id": result[0].id,
            "first_name": result[0].first_name,
            "last_name": result[0].last_name,
            "email": result[0].email,
            "password": result[0].password,
            "created_at": result[0].created_at.strftime(User.datetime_format),
            "updated_at": result[0].updated_at.strftime(User.datetime_format)
        })

        return jsonify(output)

    @staticmethod
    def create():
        """ Class method that creates a new user"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()
        if 'email' not in data:
            abort(400, "Missing email")
        if 'password' not in data:
            abort(400, "Missing password")

        try:
            new_user = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                password=data["password"]
            )
        except ValueError as exc:
            return repr(exc) + "\n"

        email = storage.get('User', '_User__email', data["email"])
        if email is not None:
            abort(400, "Cannot create user! Email already exists.")

        output = {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "created_at": new_user.created_at.strftime(User.datetime_format),
            "updated_at": new_user.updated_at.strftime(User.datetime_format)
        }

        try:
            storage.add(new_user)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new User!"

        return jsonify(output)

    @staticmethod
    def update(user_id):
        """ Class method that updates an existing user"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        try:
            # update the User record. Only first_name and last_name can be changed
            result = storage.update('User', user_id, data, User.can_update_list)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified user!"

        output = {
            "id": result.id,
            "first_name": result.first_name,
            "last_name": result.last_name,
            "email": result.email,
            "created_at": result.created_at.strftime(User.datetime_format),
            "updated_at": result.updated_at.strftime(User.datetime_format)
        }

        # print out the updated user details
        return jsonify(output)
