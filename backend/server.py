""" Implementation for server.py """

import multiprocessing
import time

from json import dumps
from flask import Flask, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from blueprints.review_route import review
from blueprints.movie_route import movie
from blueprints.user_route import user
from blueprints.message_route import message

from user.auth import Authorise
import movie.movie_details as MovieDetails
import movie.movie_homepage as MovieHomepage
import movie.person_details as PersonDetails
import user.email_recommend as EmailRecommend


def default_handler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, default_handler)
auth = Authorise(1800)


@APP.route("/clean/", methods=["POST"])
def server_auth_clean():
    """ A http funtion that clean all user data """
    try:
        info = auth.clear_all_user_data()
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@APP.route("/login/", methods=["POST"])
def server_auth_login():
    """ A http funtion that do auth_login """
    try:
        payload = request.get_json()
        info = auth.auth_login(
            payload.get("u_email"),
            payload.get("u_password")
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@APP.route("/logout/", methods=["POST"])
def server_auth_logout():
    """ A http funtion that do auth_logout """
    try:
        payload = request.get_json()
        info = auth.auth_logout(payload.get("u_token"))
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@APP.route("/register/", methods=["POST"])
def server_auth_register():
    """ A http funtion that do temp_auth_register """
    try:
        payload = request.get_json()
        info = auth.temp_auth_register(
            payload.get("u_username"),
            payload.get("u_email"),
            payload.get("u_password")
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@APP.route("/verify/email", methods=["POST"])
def server_verify_email():
    """ A http funtion that verify the user email """
    try:
        payload = request.get_json()
        info = auth.verify_email(
            payload.get("u_id"),
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@APP.route("/passwordreset/request", methods=["POST"])
def server_auth_passwordreset_request():
    """ A http function will send the rest_code to user's email """
    try:
        payload = request.get_json()
        info = auth.auth_passwordreset_request(payload.get("u_email"))
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@APP.route("/passwordreset/reset", methods=["POST"])
def server_auth_password_reset():
    """ A http function will reset the user's password """
    try:
        payload = request.get_json()
        info = auth.auth_password_reset(payload.get(
            "u_reset_code"), payload.get("u_password"))
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@APP.route("/moviedetails", methods=["GET"])
def server_movie_details():
    """ A http function that get movie details """
    try:
        payload = request.args
        info = MovieDetails.movie_details(payload.get("m_id"))
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@APP.route("/homepagemovie", methods=["GET"])
def server_homepage_movie():
    """ A http function that get the movie for the website homepage """
    try:
        payload = request.args
        info = MovieHomepage.movie_homepage(payload.get("u_id"))
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@APP.route("/actor", methods=['GET'])
def server_person_detail():
    """ A http function that get the actor/person details """
    try:
        payload = request.args
        info = PersonDetails.get_person_detail(payload.get("p_id"))
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@APP.route("/actor/expand/bio", methods=['GET'])
def server_person_expand_bio():
    """ A http function that get the actor/person full biography """
    try:
        payload = request.args
        info = PersonDetails.expand_biography(payload.get("p_id"))
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


APP.register_blueprint(user, url_prefix='/user')
APP.register_blueprint(movie, url_prefix='/movie')
APP.register_blueprint(review, url_prefix='/review')
APP.register_blueprint(message, url_prefix='/user/message')


def run_server():
    """ A function that run the server on port 8000 """
    APP.run(port=8000)


def run_email_recommend():
    """
    This function will call recommend_newly_release_movie()
    once every a week
    """
    one_week = 60*60*24*7
    while True:
        EmailRecommend.recommend_newly_release_movie()
        time.sleep(one_week)


def debug_only():
    APP.run(port=8000, debug=True)


if __name__ == "__main__":
    t1 = multiprocessing.Process(target = run_server)
    t2 = multiprocessing.Process(target = run_email_recommend)
    t1.start()
    t2.start()
