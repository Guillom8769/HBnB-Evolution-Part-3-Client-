#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

api_routes = Blueprint('api_routes', __name__, url_prefix='/api/v1')

from api.v1.amenities import *
from api.v1.cities import *
from api.v1.countries import *
from api.v1.places import *
from api.v1.reviews import *
from api.v1.users import *
