""" Implementation for review_route.py """

from flask import Blueprint, request
from json import dumps
from werkzeug.exceptions import HTTPException

import movie.movie_review as MovieReview


review = Blueprint('review', __name__)


@review.route("/post", methods=['POST'])
def server_post_review():
    """ A http function that post review """
    try:
        payload = request.get_json()
        info = MovieReview.post_review(
            payload.get("u_token"),
            payload.get("m_id"),
            payload.get("u_text"),
            payload.get("u_rate"),
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@review.route("/get", methods=['GET'])
def server_get_review():
    """ A http function that get all review """
    try:
        payload = request.args
        info = MovieReview.get_movie_review(
            payload.get("u_token"),
            payload.get("m_id"))
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@review.route("/react", methods=['POST'])
def server_review_react():
    """ A http function that react on the correspond review """
    try:
        payload = request.get_json()
        info = MovieReview.review_react(
            payload.get("u_token"),
            payload.get("r_id"),
            payload.get("ra_id"))
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code
