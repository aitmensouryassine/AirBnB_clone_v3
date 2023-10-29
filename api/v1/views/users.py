#!/usr/bin/python3
"""
View for Users objects that handles
all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def users():
    """Method to get all users"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users]), 200


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """Method to get user by using id"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    return jsonify(user.to_dict()), 200


@app_views.route("/users/<user_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Method to delete user by using id"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route("/users",
                 methods=["POST"], strict_slashes=False)
def create_user():
    """Method to create a new user"""
    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    if "email" not in data:
        abort(400, "Missing email")

    if "password" not in data:
        abort(400, "Missing password")

    user = User(**data)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>",
                 methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Method to update a user by using id"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key in ["id", "created_at", "updated_at", "email"]:
            continue
        setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
