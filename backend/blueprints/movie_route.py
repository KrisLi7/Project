""" Implementation for movie_route.py """

from json import dumps
from flask import Blueprint, request
from werkzeug.exceptions import HTTPException

import movie.movie_advanced_search as AdvanceSearch
import movie.movie_search as MovieSearch
import user.user_profile as Profile


movie = Blueprint('movie', __name__)


@movie.route("/homesearch", methods=['GET'])
def server_movie_home_search():
    """ A http function that search movie on homepage"""
    try:
        payload = request.args

        info = MovieSearch.movie_search(payload.get("keyword"))
        print(info)
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@movie.route("/searchfinity", methods=['GET'])
def server_movie_search_finity():
    """ A http function that search all movie that correspond to the keyword """
    try:
        payload = request.args
        info = MovieSearch.movie_search(payload.get("keyword"))
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@movie.route("/advancedsearch", methods=['GET'])
def server_movie_advanced_search():
    """ A http function that do advance movie search """
    try:
        payload = request.args
        info = AdvanceSearch.movie_advanced_search(
            payload.get("title"),
            payload.get("actor"),
            payload.get("director"),
            payload.get("country"),
            payload.get("r18"),
            payload.get("year"),
            payload.get("genre")
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@movie.route("/wishlist/remove", methods=['POST'])
def server_remove_from_wishlist():
    """ A http function that remove a movie from wishlist """
    try:
        payload = request.get_json()
        info = Profile.user_profile_remove_from_wishlist(
            payload.get("u_token"),
            payload.get("m_id"),
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@movie.route("/wishlist/add", methods=['POST'])
def server_add_to_wishlist():
    """ A http function that add a movie to wishlist """
    try:
        payload = request.get_json()
        info = Profile.user_profile_add_to_wishlist(
            payload.get("u_token"),
            payload.get("m_id"),
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@movie.route("/wishlist/check", methods=['GET'])
def server_check_is_in_wishlist():
    """ A http function that check is the movie in the wishlist """
    try:
        payload = request.args
        info = Profile.check_is_in_wish_list(
            payload.get("u_token"),
            payload.get("m_id"),
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code
