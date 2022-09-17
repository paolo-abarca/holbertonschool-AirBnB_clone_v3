#!/usr/bin/python3
""" Creates an url route for blueprint """

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route("/status")
def status():
    """ Route returns "status": "OK" """
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stats():
    """ retrieves the number of each objects by type """
    dict_result = {}

    obj = {"Amenity": "amenities",
           "City": "cities",
           "Place": "places",
           "Review": "reviews",
           "State": "states",
           "User": "users"}

    for keys, values in obj.items():
        count = storage.count(keys)
        dict_result[values] = count

    return jsonify(dict_result)
