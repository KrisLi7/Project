""" Implementation for user_route.py """

from json import dumps
from flask import Blueprint, request
from werkzeug.exceptions import HTTPException

import user.user_message as UserMessage

message = Blueprint('message', __name__)


@message.route("/delete", methods=['POST'])
def server_user_message_delete():
    """
    A http function that get all the message for the correspond user
    """
    try:
        payload = request.get_json()
        info = UserMessage.delete_message(
            payload.get("ms_id"),
            payload.get("u_token")
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code


@message.route("/collect", methods=['POST'])
def server_user_message_collect():
    """
    A http function that get all the message for the correspond user
    """
    try:
        payload = request.get_json()
        info = UserMessage.get_all_message(
            payload.get("u_token")
        )
        return dumps(info)
    except HTTPException as e:
        return dumps(e.description), e.code
