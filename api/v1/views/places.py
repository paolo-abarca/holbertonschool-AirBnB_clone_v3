#!/usr/bin/python3
"""
Create a new view for Place objects that handles
all default RESTFul API actions
"""

from os import abort
from api.v1.views import app_views, storage
from flask import jsonify, abort, request
from models.place import Place
from models.city import City


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def cities_id_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    query = storage.get(City, city_id)

    if query is not None:
        newList = []
        for place in query.places:
            newList.append(place.to_dict())
        return jsonify(newList)
    abort(404)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def places_id(place_id):
    """
    Retrieves a Place object
    """
    placeID = storage.get(Place, place_id)

    if placeID is not None:
        return jsonify(placeID.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place_id(place_id):
    """
    Deletes a Place object
    """
    place = storage.get(Place, place_id)

    if place is not None:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_create(city_id):
    """
    Creates a place
    """
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", place_json["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in place_json:
        abort(400, 'Missing user_id')
    if "name" not in place_json:
        abort(400, 'Missing name')

    place_json["city_id"] = city_id

    new_place = Place(**place_json)
    new_place.save()
    resp = jsonify(new_place.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """
    Updates a Place object
    """
    place = storage.get(Place, place_id)
    transform = request.get_json()

    if place is None:
        abort(404)
    elif transform is None:
        return jsonify({'error': 'Not a JSON'}), 400
    else:
        keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in transform.items():
            if key not in keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
