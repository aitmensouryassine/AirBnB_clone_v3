#!/usr/bin/python3
"""
View for amenities objects that handles
GET DELETE POST actions
"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.user import User
from flask import abort, jsonify, request


@app_views.get("/places/<place_id>/amenities", strict_slashes=False)
def place_amenities(place_id):
    """Method to get all place amenities"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify([amenity.to_dict()
                    for amenity in place.amenities]), 200


@app_views.delete("/places/<place_id>/amenities/<amenity_id>",
                  strict_slashes=False)
def delete_amenity_linked_to_place(place_id, amenity_id):
    """delete amenity linked to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.post("places/<place_id>/amenities/<amenity_id>")
def link_amenity(place_id, amenity_id):
    """link amenity to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    amenity.place_id = place.id
    storage.save()

    return jsonify(amenity.to_dict()), 201
