#!/usr/bin/python3
"""
View for reviews objects that handles
all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flask import abort, jsonify, request


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def place_reviews(place_id):
    """Method to get all place reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify([review.to_dict()
                    for review in place.reviews]), 200


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """Method to get review by using id"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Method to delete review by using id"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Method to create a new review"""
    place = storage.get(Place, place_id)
    if place is None:
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

    if "text" not in data:
        abort(400, "Missing text")

    review = Review(**data)
    setattr(review, "place_id", place_id)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Method to update a review by using id"""
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]

    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key in ignore:
            continue
        setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
