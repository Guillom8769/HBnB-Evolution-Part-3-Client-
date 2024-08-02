#!/usr/bin/python
""" Review model """

from datetime import datetime
import uuid
from flask import jsonify, request, abort
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from data import storage, Base

class Review(Base):
    """Representation of review """

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
    can_init_list = ["place_id", "user_id", "rating", "comment"]
    can_update_list = ["rating", "comment"]

    # Class attrib defaults
    __tablename__ = 'reviews'
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    __place_id = Column("place_id", String(60), ForeignKey('places.id'), nullable=False)
    __user_id = Column("user_id", String(60), ForeignKey('users.id'), nullable=False)
    __rating = Column("rating", Integer, nullable=False, default=0)
    __comment = Column("comment", String(1024), nullable=False)
    place_r = relationship("Place", back_populates="reviews_r")
    user_r = relationship("User", back_populates="reviews_r")

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
    def place_id(self):
        """ Return private prop place_id """
        return self.__place_id

    @place_id.setter
    def place_id(self, value):
        """Setter for private prop place_id"""
        self.__place_id = value

    @property
    def user_id(self):
        """ Return private prop place_id """
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        """Setter for private prop user_id"""
        self.__user_id = value

    @property
    def rating(self):
        """ Return private prop rating """
        return self.__rating

    @rating.setter
    def rating(self, value):
        """Setter for private prop rating"""
        if isinstance(value, int):
            self.__rating = value
        else:
            raise ValueError("Invalid value specified for Rating: {}".format(value))

    @property
    def comment(self):
        """ Return private prop comment """
        return self.__comment

    @comment.setter
    def comment(self, value):
        """Setter for private prop comment"""
        # Can't think of any special checks to perform here tbh
        self.__comment = value

    # --- Static methods ---
    @staticmethod
    def all(return_raw_result = False):
        """ Class method that returns all reviews data"""
        output = []

        try:
            result = storage.get('Review')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load reviews!"

        if return_raw_result:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "place_id": row.place_id,
                "user_id": row.user_id,
                "rating": row.rating,
                "comment": row.comment,
                "created_at": row.created_at.strftime(Review.datetime_format),
                "updated_at": row.updated_at.strftime(Review.datetime_format)
            })

        return jsonify(output)

    @staticmethod
    def specific(review_id):
        """ Class method that returns a specific review's data"""
        try:
            result: Review = storage.get('Review', 'id', review_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Review data!"

        output = {
            "id": result[0].id,
            "place_id": result[0].place_id,
            "user_id": result[0].user_id,
            "rating": result[0].rating,
            "comment": result[0].comment,
            "created_at": result[0].created_at.strftime(Review.datetime_format),
            "updated_at": result[0].updated_at.strftime(Review.datetime_format)
        }

        return jsonify(output)

    @staticmethod
    def create():
        """ Class method that creates a new review"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        # Make sure everything we need is in the request payload
        for k in Review.can_init_list:
            if k not in data:
                abort(400, "Unable to create new Place! Missing attribute {}.".format(k))

        try:
            new_review = Review(
                place_id=data["place_id"],
                user_id=data["user_id"],
                rating=data["rating"],
                comment=data["comment"]
            )
        except ValueError as exc:
            return repr(exc) + "\n"

        try:
            storage.add(new_review)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Review!"

        output = {
            "id": new_review.id,
            "place_id": new_review.place_id,
            "user_id": new_review.user_id,
            "rating": new_review.rating,
            "comment": new_review.comment,
            "created_at": new_review.created_at.strftime(Review.datetime_format),
            "updated_at": new_review.updated_at.strftime(Review.datetime_format)
        }

        return jsonify(output)

    @staticmethod
    def update(review_id):
        """ Class method that updates an existing review"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        review_data: Review = storage.get('Review', 'id', review_id)
        if review_data is None:
            abort(400, "Review not found for id {}".format(review_id))

        try:
            # update the Review record.
            result = storage.update('Review', review_data.id, data, Review.can_update_list)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified review!"

        output = {
            "id": result.id,
            "place_id": result.place_id,
            "user_id": result.user_id,
            "rating": result.rating,
            "comment": result.comment,
            "created_at": result.created_at.strftime(Review.datetime_format),
            "updated_at": result.updated_at.strftime(Review.datetime_format)
        }

        return jsonify(output)
