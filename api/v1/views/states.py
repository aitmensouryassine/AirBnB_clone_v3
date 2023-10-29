#!/usr/bin/python3
"""
View for State objects that handles all
default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, jsonify, request


@app_views.route("/states", methods=["GET"],
                 strict_slashes=False)
def states():
    """Method to get all the states"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states]), 200


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def state(state_id):
    """Method to get a state by id"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    return jsonify(state.to_dict()), 200


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Method to delete a state by using id"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return jsonify({}), 200


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def create_state():
    """Method to create a new state"""
    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    if "name" not in data:
        abort(400, "Missing name")

    state = State(**data)
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """Method to update a state"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
