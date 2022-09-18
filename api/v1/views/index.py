#!/usr/bin/python3
""" Creates an url route for blueprint """

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """ Route returns "status": "OK" """
    return jsonify({"status": "OK"})
