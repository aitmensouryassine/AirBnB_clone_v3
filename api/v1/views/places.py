#!/usr/bin/python3
"""
View for places objects that handles
all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from flask import abort, jsonify, request


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def city_places(city_id):
    """Method to get all city places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = storage.all(Place).values()
    return jsonify([place.to_dict() for place in places
                    if place.city_id == city_id]), 200


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """Method to get place by using id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict()), 200


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Method to delete place by using id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Method to create a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    if "user_id" not in data:
        abort(400, "Missing user_id")

    user_id = data.get("user_id")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if "name" not in data:
        abort(400, "Missing name")

    place = Place(**data)
    setattr(place, "city_id", city_id)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """Method to update a place by using id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            continue
        setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def search_places():
    """Method that retrieves all Place objects depending of
    the JSON in the body of the request
    """
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    states_list = data.get("states", [])
    cities_list = data.get("cities", [])
    amenities_list = data.get("amenities", [])

    if not data or not len(data) or (not len(states_list) and
                                     not len(cities_list) and
                                     not len(amenities_list)):
        places = [place.to_dict() for place in storage.all(Place).values()]
        return jsonify(places), 200

    states = [storage.get(State, id) for id in states_list]
    cities = [storage.get(City, id) for id in cities_list]
    amenities = [storage.get(Amenity, id) for id in amenities_list]

    places = []
    for state in states:
        if state:
            for city in state.cities:
                for place in city.places:
                    places.append(place)

    for city in cities:
        if city:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if len(amenities) != 0:
        if not len(places):
            places = storage.all(Place).values()
        places = [place for place in places
                  if all(amenity in place.amenities for amenity in amenities)]

    result = []
    for place in places:
        p_dict = place.to_dict()
        p_dict.pop('amenities', None)
        result.append(p_dict)
    return jsonify(result), 200
