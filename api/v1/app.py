#!/usr/bin/python3
""" Status of your API """

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_appcontext(self):
    """ Method for the close session """
    storage.close()


@app.errorhandler(404)
def error_handler(exception):
    """ create a handler for 404 errors a JSON """
    response = {"error": "Not found"}
    return jsonify(response), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST"),
            port=getenv("HBNB_API_PORT"),
            threaded=True)
