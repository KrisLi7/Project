""" Implementation for user_message.py """

import sqlite3

from threading import Timer
import user.user_util as UserUtil
from user.email import Email
from error import InputError, AccessError


def check_mess_send_to_which_us(m_id, u_id_send, username_send):
    """
    A function that will send email notification and frontend message
    to eligible user.
    Eligible user means:
        User who post the review message was not in the bannedlist of the
        user who receive this message
        The movie of the review is in the wishlist of the
        user who receive this message
        The email notification of the user who receive this message is on

    Args:
        m_id: A string of a movie id
        u_id_send: A string of user id (from the user who post review)
        username_send: A string of username (from the user who post review)

    Returns:
        A dictionary that contain the success message

    Raises:
        Since this function will only be called from post_review(),
        so any exception will be handled in post_review()
    """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    query = """
        SELECT wu.u_token, wu.u_id, wu.u_email, wu.u_username
        FROM web_user wu
        LEFT JOIN user_wishlist uw ON wu.u_id = uw.u_id
        WHERE wu.u_notification = 1
        AND uw.m_id = '{}'
        AND wu.u_id <> '{}'
    """.format(m_id, u_id_send)
    cur.execute(query)
    result = cur.fetchall()
    query = "SELECT m_title from web_movie WHERE m_id = '{}'".format(m_id)
    cur.execute(query)
    m_title = cur.fetchone()[0]
    mess = '{} post a review on the movie "{}" in your wish list'.format(username_send, m_title)
    con.close()
    for user in result:
        if not UserUtil.check_is_in_banned_list(user[1], u_id_send):
            send_later = Timer(1, Email(user[2], user[3]).sendReviewMessageEmail,
                (u_id_send, username_send, m_id, m_title))
            send_later.start()
            post_review_message(user, mess, m_id)

    return {
        "is_success": True
    }


def post_review_message(user_receive, mess, m_id):
    """
    A helper function for check_mess_send_to_which_us() that will
    store the given variable into the table message_list in database
    """
    if not UserUtil.is_user_id_valid(user_receive[1]):
        raise InputError("Invalid user")

    ms_id = UserUtil.generate_message_id()
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    query = "INSERT INTO message_list(ms_id, u_id, m_id, message) VALUES (?, ?, ?, ?)"
    cur.execute(query, (ms_id, user_receive[1], m_id, mess))
    con.commit()
    con.close()


def get_all_message(token):
    """
    A function that will get all the message for the given user
    and show into frontend.

    Args:
        token: A string used to identify a user

    Returns:
        A dictionary that contain the list of message dict
        message_list = [{message info}, {message info}]

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")

    message_list = []
    u_id = UserUtil.get_uid(token)
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT * FROM message_list where u_id = '{}'".format(u_id))
    result = cur.fetchall()
    con.close()

    for message in result:
        temp_dict = {
            "ms_id": message[0],
            "m_id": message[2],
            "message": message[3]
        }
        message_list.append(temp_dict)

    return {
        "is_success": True,
        "message_list": message_list
    }


def delete_message(token, ms_id):
    """
    A function that will delete the given ms_id in the database

    Args:
        token: A string used to identify a user
        ms_id: A string of message id

    Returns:
        A dictionary that contain the success message
        and the correspond message id that get deleted

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
        InputError("Invalid message"):
            the given message id does not exist in the database
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    if not UserUtil.is_message_id_valid(ms_id):
        raise InputError("Invalid message")

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("DELETE FROM message_list where ms_id = '{}'".format(ms_id))
    con.commit()
    con.close()
    return {
        "is_success": True,
        "ms_id": ms_id
    }
