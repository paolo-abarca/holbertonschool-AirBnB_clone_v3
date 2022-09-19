#!/usr/bin/python3
"""
Create a new view for Amenity objects that
handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenities():
    """
    Retrieves the list of all Amenity objects
    """
    all_amenities = []
    amenities = storage.all("Amenity").values()

    for amenity in amenities:
        all_amenities.append(amenity.to_dict())

    return jsonify(all_amenities)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenities_id(amenity_id=None):
    """
    Retrieves a Amenity object
    """
    if amenity_id is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if amenity is not None:
        return jsonify(amenity.to_dict())

    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def amenities_delete(amenity_id=None):
    """
    Deletes a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/amenities", methods=['POST'],
                 strict_slashes=False)
def amenities_post():
    """
    Creates a Amenity
    """
    try:
        json_data = request.get_json()
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

    if json_data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    elif json_data.get('name') is None:
        return jsonify({'error': 'Missing name'}), 400
    else:
        amenity_new = Amenity(**json_data)
        storage.new(amenity_new)
        storage.save()
        return jsonify(amenity_new.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def amenities_put(amenity_id=None):
    """
    Updates a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    json_data = request.get_json()

    if amenity is None:
        abort(404)
    elif json_data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    else:
        black_list = ['id', 'created_at', 'updated_at']
        for key, value in json_data.items():
            if key not in black_list:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
