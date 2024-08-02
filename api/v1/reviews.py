""" objects that handles all default RestFul API actions for Review """
from api.v1 import api_routes
from models.review import Review


@api_routes.route('/reviews', methods=["POST"])
def review_post():
    """ Creates a new Review and returns it """
    return Review.create()

@api_routes.route('/reviews', methods=["GET"])
def review_get():
    """ Gets all Reviews """
    return Review.all()

@api_routes.route('/reviews/<review_id>', methods=["GET"])
def review_specific_get(review_id):
    """ Gets a specific Review """
    return Review.specific(review_id)

@api_routes.route('/reviews/<review_id>', methods=["PUT"])
def review_put(review_id):
    """ Updates a specific Review and returns it """
    return Review.update(review_id)
