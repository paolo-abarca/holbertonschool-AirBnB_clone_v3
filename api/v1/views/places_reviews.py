#!/usr/bin/python3
"""
    Create a new view for Review object that handles all
    default RESTFul API actions
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET'],
                 strict_slashes=False)
def place_id_reviews(place_id):
    """ endpoint to return place ids for your review """
    placeId = storage.get(Place, place_id)

    if placeId is not None:
        newList = []
        for place in placeId.reviews:
            newList.append(place.to_dict())
        return jsonify(newList)
    abort(404)


@app_views.route("/reviews/<review_id>",
                 methods=['GET'],
                 strict_slashes=False)
def reviews_id(review_id):
    """ endpoint to return review id """
    reviewId = storage.get(Review, review_id)

    if reviewId is not None:
        return jsonify(reviewId.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ endpoint to delete according to its review id """
    reviewId = storage.get(Review, review_id)

    if reviewId is not None:
        storage.delete(reviewId)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/places/<place_id>/reviews",
                 methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ end point to add new review according to their given places """
    placeId = storage.get(Place, place_id)

    try:
        data_json = request.get_json()
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

    userId = storage.get(User, data_json.get('user_id'))

    if placeId is None:
        abort(404)
    elif data_json is None:
        return jsonify({'error': 'Not a JSON'}), 400
    elif data_json.get('user_id') is None:
        return jsonify({'error': 'Missing user_id'}), 400
    elif userId is None:
        abort(404)
    elif data_json.get('text') is None:
        return jsonify({'error': 'Missing text'}), 400
    else:
        newReview = Review(**data_json)
        newReview.place_id = place_id
        storage.new(newReview)
        storage.save()
        return jsonify(newReview.to_dict()), 201


@app_views.route("/reviews/<review_id>",
                 methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """ end point to update review """

    reviewId = storage.get(Review, review_id)
    data_json = request.get_json()

    if reviewId is None:
        abort(404)
    elif data_json is None:
        return jsonify({'error': 'Not a JSON'}), 400
    else:
        keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in data_json.items():
            if key not in keys:
                setattr(reviewId, key, value)
        reviewId.save()
        return jsonify(reviewId.to_dict()), 200
