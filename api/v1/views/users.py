#!/usr/bin/python3
""" Users Api Rest """


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'],
                 strict_slashes=False)
def all_users():
    """ endpoint to return all users """
    new_users = []
    users = storage.all(User).values()

    for user in users:
        new_users.append(user.to_dict())

    return jsonify(new_users)


@app_views.route("/users/<user_id>",
                 methods=['GET'],
                 strict_slashes=False)
def get_user_id(user_id):
    """ endpoint to return user ids """
    userId = storage.get(User, user_id)

    if userId is not None:
        return jsonify(userId.to_dict())
    abort(404)


@app_views.route("/users/<user_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user_id(user_id):
    """ endpoint to delete according to its user id """
    userId = storage.get(User, user_id)

    if userId is not None:
        storage.delete(userId)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/users",
                 methods=['POST'],
                 strict_slashes=False)
def post_users():
    """ end point to add new users """
    try:
        json_data = request.get_json()
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

    if json_data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    elif json_data.get('email') is None:
        return jsonify({'error': 'Missing email'}), 400
    elif json_data.get('password') is None:
        return jsonify({'error': 'Missing password'}), 400
    else:
        newUser = User(**json_data)
        storage.new(newUser)
        storage.save()
        return jsonify(newUser.to_dict()), 201


@app_views.route("/users/<user_id>",
                 methods=['PUT'],
                 strict_slashes=False)
def put_users_id(user_id):
    """ end point to update users """
    userId = storage.get(User, user_id)
    json_data = request.get_json()

    if userId is None:
        abort(404)
    elif json_data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    else:
        keys = ['id', 'email', 'created_at', 'updated_at']
        for key, value in json_data.items():
            if key not in keys:
                setattr(userId, key, value)
        userId.save()
        return jsonify(userId.to_dict()), 200
