""" Implementation for user_profile.py """

import sqlite3

from threading import Timer

import user.user_util as UserUtil
import movie.movie_util as MovieUtil
import movie.movie_details as MovieDetails
from user.email import Email
from error import InputError, AccessError



def user_profile(token):
    """
    For a valid user, returns information about
    their userName, email, first name and last name, and other info

    Args:
        token: A string used to identify a user

    Returns:
        A dictionary that contain the all the information for the user

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    u_id = UserUtil.get_uid(token)

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT * FROM web_user where u_id = ?"), (u_id,))
    result = cur.fetchone()

    u_is_critic_reviewer = UserUtil.convert_int_to_boolean(result[10])
    u_notification = UserUtil.convert_int_to_boolean(result[12])
    info_dict = {
        "u_id": result[0],
        "u_username": result[2],
        "u_email": result[4],
        "u_avatar": result[5],
        "u_lastname": result[6],
        "u_firstname": result[7],
        "u_level": result[8],
        "u_exp": result[9],
        "u_is_critic_reviewer": u_is_critic_reviewer,
        "u_notification": u_notification,
    }

    wish_list = []
    query = """
        SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating, a.m_year
        FROM web_movie a, user_wishlist b
        WHERE a.m_id = b.m_id
        AND b.u_id = "{}"
        ORDER BY a.m_rating DESC
    """.format(u_id)
    cur.execute(query)
    for result in cur.fetchall():
        average = MovieDetails.get_average(result[0])
        result_dict = {
            'm_id': result[0],
            'm_title': result[1],
            'm_poster': result[2],
            "m_imdb_rate": result[3],
            "m_year": result[4],
            "m_web_rate": average
        }
        wish_list.append(result_dict)

    banned_list = []
    query = """
        SELECT distinct a.u_id, a.u_username, a.u_avatar
        FROM web_user a, user_bannedlist b
        WHERE b.banned_u_id = a.u_id
        AND b.u_id = "{}"
    """.format(u_id)
    cur.execute(query)
    for result in cur.fetchall():
        result_dict = {
            'u_id': result[0],
            'u_username': result[1],
            'a.u_avatar': result[2],
        }
        banned_list.append(result_dict)

    info_dict["u_wishlist"] = wish_list
    info_dict["u_banned_list"] = banned_list

    con.close()
    return info_dict


def get_visitor_profile(token, u_id_visit):
    """
    For a user visiting other user's profile, returns information about
    their userName, email, first name and last name, and other info

    Args:
        token: A string used to identify a user (login user, will be empty string if is not login)
        u_id_visit: A string of user id (u_id correspond to the user that get visit)

    Returns:
        A dictionary that contain the all the information for the user
        getting visit

    Raises:
        AccessError("Invalid user")
            the given token does not match any user in the database
        InputError("Invalid user id")
            the given user id does not match any user in the database
    """
    if not UserUtil.is_user_id_valid(u_id_visit):
        raise InputError("Invalid user id")
    if len(token) == 0:
        u_is_banned = False
    else:
        if not UserUtil.is_token_valid(token):
            raise AccessError("Invalid user")
        u_id = UserUtil.get_uid(token)
        u_is_banned = UserUtil.check_is_in_banned_list(u_id, u_id_visit)

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT * FROM web_user where u_id = ?"), (u_id_visit,))
    result = cur.fetchone()

    u_is_critic_reviewer = UserUtil.convert_int_to_boolean(result[10])
    info_dict = {
        "u_id": result[0],
        "u_username": result[2],
        "u_email": result[4],
        "u_avatar": result[5],
        "u_lastname": result[6],
        "u_firstname": result[7],
        "u_level": result[8],
        "u_exp": result[9],
        "u_is_critic_reviewer": u_is_critic_reviewer,
        "u_is_banned": u_is_banned,
    }

    wish_list = []
    query = """
            SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating, a.m_year
            FROM web_movie a, user_wishlist b
            WHERE a.m_id = b.m_id
            AND b.u_id = "{}"
            ORDER BY a.m_rating DESC
        """.format(u_id_visit)
    cur.execute(query)
    for result in cur.fetchall():
        result_dict = {
            'm_id': result[0],
            'm_title': result[1],
            'm_poster': result[2],
            "m_imdb_rate": result[3],
            "m_year": result[4],
        }
        wish_list.append(result_dict)
    con.close()
    info_dict["u_wishlist"] = wish_list
    return info_dict


def user_profile_change_email(token, email):
    """
    Update the authorised user's email address

    Args:
        token: A string used to identify a user
        email: A string of email

    Returns:
        A dictionary that contain the success message

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
        InputError("Invalid email"):
            the given email is not in the correct format
        InputError("Used email"):
            the given email is used by other user
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    if not UserUtil.is_email_valid(email):
        raise InputError("Invalid email")
    if UserUtil.is_email_used(email):
        raise InputError("Used email")
    if UserUtil.is_email_used_temp_data(email):
        raise InputError("Used email")

    u_id = UserUtil.get_uid(token)
    u_username = UserUtil.get_user_info(u_id).get("u_username")
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    query = """
        UPDATE web_user SET u_is_verify = 0,
        u_email = '{}'
        WHERE u_token = '{}'
    """.format(email, token)
    cur.execute(query)
    con.commit()
    con.close()

    user_dict = {
        "u_id": u_id,
        "u_email": email
    }
    UserUtil.delete_temp_user_detail(u_id)
    UserUtil.append_temp_user(user_dict)
    send_later = Timer(1, Email(email, u_username).sendVerifyEmailForChangeEmail, (u_id,))
    send_later.start()
    return {
        'is_success': True,
        'message': "Change email success, a verification is sent to " + email
    }


def user_profile_change_username(token, username):
    """
    Update the authorised user's username

    Args:
        token: A string used to identify a user
        username: A string of username

    Returns:
        A dictionary that contain the success message

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
        AccessError("Please verify your email"):
            the given user has not verify their email after they request to change email
        InputError("Invalid username")
            the given username is not in the correct format
        InputError("Used username")
            the given username is used by other user
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    if not UserUtil.is_user_email_verify(token):
        raise AccessError("Please verify your email")
    if not UserUtil.is_username_in_range(username):
        raise InputError("Invalid username")
    if UserUtil.is_username_used(username):
        raise InputError("Used username")
    if UserUtil.is_username_used_temp_data(username):
        raise InputError("Used username")

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("UPDATE web_user SET u_username = ? where u_token = ?"), (username, token))
    con.commit()
    con.close()
    return {
        'is_success': True,
        'message': "Change user name success"
    }


def user_profile_change_firstname(token, firstname):
    """
    Update the authorised user's first name

    Args:
        token: A string used to identify a user
        firstname: A string of firstname

    Returns:
        A dictionary that contain the success message

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
        AccessError("Please verify your email"):
            the given user has not verify their email after they request to change email
        InputError("Invalid name")
            the given first name is not in the correct format
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    if not UserUtil.is_user_email_verify(token):
        raise AccessError("Please verify your email")
    if not UserUtil.is_name_in_range(firstname):
        raise InputError("Invalid name")

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("UPDATE web_user SET u_firstname = ? where u_token = ?"), (firstname, token))
    con.commit()
    con.close()
    return {
        'is_success': True,
        'message': "Change first name success"
    }


def user_profile_change_lastname(token, lastname):
    """
    Update the authorised user's last name

    Args:
        token: A string used to identify a user
        lastname: A string of lastname

    Returns:
        A dictionary that contain the success message

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
        AccessError("Please verify your email"):
            the given user has not verify their email after they request to change email
        InputError("Invalid name")
            the given last name is not in the correct format
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    if not UserUtil.is_user_email_verify(token):
        raise AccessError("Please verify your email")
    if not UserUtil.is_name_in_range(lastname):
        raise InputError("Invalid name")

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("UPDATE web_user SET u_lastname = ? where u_token = ?"), (lastname, token))
    con.commit()
    con.close()
    return {
        'is_success': True,
        'message': "Change last name success"
    }


def user_profile_change_avatar(token, img_url):
    """
    Upload/change a profile image

    Args:
        token: A string used to identify a user
        img_url: A img_url in a base64 format

    Returns:
        A dictionary that contain the success message

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
        AccessError("Please verify your email"):
            the given user has not verify their email after they request to change email
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    if not UserUtil.is_user_email_verify(token):
        raise AccessError("Please verify your email")

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("UPDATE web_user SET u_avatar = ? where u_token = ?"), (img_url, token))
    con.commit()
    con.close()
    return {
        'is_success': True,
        'message': "Change user's photo success"
    }


def user_profile_change_notification_status(token, notification_bool):
    """
    Change the given user's email notification status

    Args:
        token: A string used to identify a user
        notification_bool: A boolean specified the user want the
        email notification to be on/off

    Returns:
        A dictionary that contain the success message

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
        AccessError("Please verify your email"):
            the given user has not verify their email after they request to change email
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    if not UserUtil.is_user_email_verify(token):
        raise AccessError("Please verify your email")

    if notification_bool:
        message = "Email notification is on!"
        u_notification = 1
    else:
        message = "Email notification is off!"
        u_notification = 0

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("UPDATE web_user SET u_notification = ? where u_token = ?"), (u_notification, token))
    con.commit()
    con.close()

    return {
        'is_success': True,
        'message': message
    }


def user_profile_add_to_wishlist(token, m_id):
    """
    Remove movie with m_id from wishlist

    Args:
        token: A string used to identify a user
        m_id: A string of movie id

    Returns:
        A dictionary that contain the success message

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
        AccessError("Movie not exist in database"):
            the given movie id is not exist in the database
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    if not MovieUtil.is_movie_exist(m_id):
        raise AccessError("Movie not exist in database")

    u_id = UserUtil.get_uid(token)
    uw_id = UserUtil.generate_wishlist_id()

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("""
        INSERT INTO user_wishlist(uw_id, u_id, m_id)
        VALUES(?, ?, ?)
    """, (uw_id, u_id, m_id))
    con.commit()
    cur.close()

    return {
        'is_success': True,
        'message': "Add to wishlist successfully"
    }


def user_profile_add_to_banned_list(token, banned_u_id):
    """
    remove user (banned_u_id) from banned_list of the requesting user (token)
    Args:
        token: A string used to identify a user
        banned_u_id: A string of user id who got banned before

    Returns:
        A dictionary that contain the success message

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
        InputError("Invalid user id")
            the given user id is not exist in the database
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    if not UserUtil.is_user_id_valid(banned_u_id):
        raise InputError("Invalid user id")

    u_id = UserUtil.get_uid(token)
    ub_id = UserUtil.generate_bannedlist_id()

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("""
        INSERT INTO user_bannedlist(ub_id, u_id, banned_u_id)
        VALUES(?, ?, ?)
    """, (ub_id, u_id, banned_u_id))
    con.commit()
    cur.close()

    return {
        'is_success': True,
        'message': "Add to banned list successfully"
    }


def user_profile_remove_from_wishlist(token, m_id):
    """
    Add movie with m_id from wishlist

    Args:
        token: A string used to identify a user
        m_id: A string of movie id

    Returns:
        A dictionary that contain the success message

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
        AccessError("Invalid movie"):
            the given movie id is not exist in the database
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    if not MovieUtil.is_movie_exist(m_id):
        raise AccessError("Invalid movie")

    u_id = UserUtil.get_uid(token)

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("""
        DELETE FROM user_wishlist
        WHERE u_id = '{}'
        AND m_id = '{}'
    """.format(u_id, m_id))
    con.commit()
    cur.close()

    return {
        'is_success': True,
        'message': "Remove from wishlist successfully"
    }


def user_profile_remove_from_banned_list(token, banned_u_id):
    """
    add user (banned_u_id) into the banned_list of the requesting user (token)
    Args:
        token: A string used to identify a user
        banned_u_id: A string of user id who needs to get banned

    Returns:
        A dictionary that contain the success message

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
        InputError("Invalid user id")
            the given user id is not exist in the database
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    if not UserUtil.is_user_id_valid(banned_u_id):
        raise InputError("Invalid user id")

    u_id = UserUtil.get_uid(token)

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("""
        DELETE FROM user_bannedlist
        WHERE u_id = '{}'
        AND banned_u_id = '{}'
    """.format(u_id, banned_u_id))
    con.commit()
    cur.close()

    return {
        'is_success': True,
        'message': "Remove from banned list successfully"
    }


def check_is_in_wish_list(token, m_id):
    """
    A function that check is the movie in wishlist

    Args:
        token: A string used to identify a user
            (if no token is provided then it will always return false)
        m_id: A string of movie id

    Returns:
        A boolean

    Raises:
        AccessError("Invalid movie"):
            the given movie id is not exist in the database
    """
    if not MovieUtil.is_movie_exist(m_id):
        raise AccessError("Invalid movie")

    if len(token) == 0:
        return False
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid token")

    u_id = UserUtil.get_uid(token)
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("""
        SELECT count(*)
        FROM user_wishlist a
        WHERE a.u_id = "{}"
        AND a.m_id = "{}"
    """.format(u_id, m_id))
    result = cur.fetchone()
    if result[0] > 0:
        return True
    else:
        return False
