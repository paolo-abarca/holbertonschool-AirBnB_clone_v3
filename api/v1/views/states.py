#!/usr/bin/python3
"""
Create a new view for State objects that handles
all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states/", methods=["GET"], strict_slashes=False)
def states():
    """
    Retrieves the list of all State objects
    """
    all_states = []
    states = storage.all("State").values()

    for state in states:
        all_states.append(state.to_dict())

    return jsonify(all_states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def states_id(state_id=None):
    """
    Retrieves a State object
    """
    if state_id is None:
        abort(404)

    states = storage.all("State").values()

    for state in states:
        if state_id == state.id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def states_delete(state_id=None):
    """
    Deletes a State object
    """
    if state_id is None:
        abort(404)

    states = storage.all("State").values()

    for state in states:
        if state_id == state.id:
            storage.delete(state)
            storage.save()

    return jsonify({}), 200


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def states_post():
    """
    Creates a State
    """
    json_data = request.get_json()

    if json_data is None:
        abort(400, "Not a JSON")

    if "name" not in json_data:
        abort(400, "Missing name")

    state_new = State(**json_data)
    state_new.save()

    return jsonify(state_new.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def states_put(state_id=None):
    """
    Updates a State object
    """
    json_data = request.get_json()

    if json_data is None:
        abort(404, "Not a JSON")

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    black_list = ["id", "created_at", "updated_at"]

    for key, value in json_data.items():
        if key not in black_list:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
