""" Implementation for user_route.py """

from json import dumps
from flask import Blueprint, request
from werkzeug.exceptions import HTTPException

import user.user_profile as Profile


user = Blueprint('user', __name__)


@user.route("/profile/", methods=['GET'])
def server_user_profile():
    """ A http function that get the correspond user details """
    try:
        payload = request.args
        info = Profile.user_profile(payload.get("u_token"))
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@user.route("/profile/visit", methods=['GET'])
def server_visitor_profile():
    """
    A http function that get the correspond user details
    (This is used when the login user is visiting other user's profile)
    """
    try:
        payload = request.args
        info = Profile.get_visitor_profile(
            payload.get("u_token"),
            payload.get("u_id_visit")
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@user.route("/profile/change/username", methods=['POST'])
def server_user_profile_change_username():
    """ A http function that change the correspond user's username """
    try:
        payload = request.get_json()
        info = Profile.user_profile_change_username(
            payload.get("u_token"),
            payload.get("u_data")
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@user.route("/profile/change/email", methods=['POST'])
def server_user_profile_change_email():
    """ A http function that change the correspond user's email """
    try:
        payload = request.get_json()
        info = Profile.user_profile_change_email(
            payload.get("u_token"),
            payload.get("u_data")
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@user.route("/profile/change/firstname", methods=['POST'])
def server_user_profile_change_firstname():
    """ A http function that change the correspond user's firstname """
    try:
        payload = request.get_json()
        info = Profile.user_profile_change_firstname(
            payload.get("u_token"),
            payload.get("u_data")
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@user.route("/profile/change/lastname", methods=['POST'])
def server_user_profile_change_lastname():
    """ A http function that change the correspond user's lastname """
    try:
        payload = request.get_json()
        info = Profile.user_profile_change_lastname(
            payload.get("u_token"),
            payload.get("u_data")
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@user.route("/profile/change/avatar", methods=['POST'])
def server_user_profile_change_avatar():
    """ A http function that change the correspond user's avatar """
    try:
        payload = request.get_json()
        info = Profile.user_profile_change_avatar(
            payload.get("u_token"),
            payload.get("u_data"),
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@user.route("/profile/change/notification", methods=['POST'])
def server_user_profile_change_notification_status():
    """
    A http function that change the correspond user's email notification status
    """
    try:
        payload = request.get_json()
        info = Profile.user_profile_change_notification_status(
            payload.get("u_token"),
            payload.get("u_data"),
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@user.route("/profile/bannedlist/add", methods=['POST'])
def server_user_profile_add_to_banned_list():
    """ A http function that add a user from banned list"""
    try:
        payload = request.get_json()
        info = Profile.user_profile_add_to_banned_list(
            payload.get("u_token"),
            payload.get("banned_u_id"),
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@user.route("/profile/bannedlist/remove", methods=['POST'])
def server_user_profile_change_banned_list():
    """ A http function that remove a user from banned list"""
    try:
        payload = request.get_json()
        info = Profile.user_profile_remove_from_banned_list(
            payload.get("u_token"),
            payload.get("banned_u_id"),
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code
