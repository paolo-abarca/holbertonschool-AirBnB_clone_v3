#!/usr/bin/python3
"""
Create a new view for Place objects that handles
all default RESTFul API actions
"""

from os import abort
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
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


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """
    Creates a Place
    """
    try:
        transform = request.get_json()
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

    if not storage.get("User", transform["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in transform:
        return jsonify({'error': 'Missing user_id'}), 400
    if "name" not in transform:
        return jsonify({'error': 'Missing name'}), 400

    transform["city_id"] = city_id

    newPlace = Place(**transform)
    storage.new(newPlace)
    storage.save()
    return jsonify(newPlace.to_dict()), 201


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
