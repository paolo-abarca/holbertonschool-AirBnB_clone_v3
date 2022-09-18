#!/usr/bin/python3
""" City Api Rest """

from os import abort
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def states_id_cities(state_id):
    """ endpoint to return state ids for your city """
    query = storage.get(State, state_id)

    if query is not None:
        newList = []
        for city in query.cities:
            newList.append(city.to_dict())
        return jsonify(newList)
    abort(404)


@app_views.route("/cities/<city_id>", methods=['GET'])
def cities_id(city_id):
    """ endpoint to return city ids """
    cityID = storage.get(City, city_id)

    if cityID is not None:
        return jsonify(cityID.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city_id(city_id):
    """ endpoint to delete according to its cities id """
    city = storage.get(City, city_id)

    if city is not None:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def post_city(state_id):
    """ end point to add new cities according to their given state """
    state = storage.get(State, state_id)
    transform = request.get_json()

    if state is None:
        abort(404)
    elif transform is None:
        return jsonify({'error': 'Not a JSON'}), 400
    elif transform.get('name') is None:
        return jsonify({'error': 'Missing name'}), 400
    else:
        newCity = City(**transform)
        newCity.state_id = state_id
        storage.new(newCity)
        storage.save()
        return jsonify(newCity.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'])
def put_city(city_id):
    """ end point to update cities """
    city = storage.get(City, city_id)
    transform = request.get_json()

    if city is None:
        abort(404)
    elif transform is None:
        return jsonify({'error': 'Not a JSON'}), 400
    else:
        keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in transform.items():
            if key not in keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
