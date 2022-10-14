"""
Implementation for user_util.py
It contains all the helper functions for user
"""

import hashlib
import re
import sqlite3
import jwt

from memory.authData import USER_DATA


secret = "plznobug"


def generate_password(password):
    """ Generate password """
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token(username, email):
    """ Generate token """
    jwt_info = {"username": username, "email": email}
    return jwt.encode(jwt_info, secret, algorithm="HS256")


def generate_message_id():
    """ Generate a message id """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT MAX(ms_id) FROM message_list")
    result = cur.fetchone()
    con.close()
    if result[0] is None:
        ms_id = "ms" + "1".zfill(7)
    else:
        num = int(result[0].strip("ms")) + 1
        ms_id = "ms" + str(num).zfill(7)
    return ms_id

def generate_wishlist_id():
    """ Generate a wishlist id """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT MAX(uw_id) FROM user_wishlist")
    result = cur.fetchone()
    con.close()
    if result[0] is None:
        uw_id = "uw" + "1".zfill(7)
    else:
        num = int(result[0].strip("uw")) + 1
        uw_id = "uw" + str(num).zfill(7)
    return uw_id

def generate_bannedlist_id():
    """ Generate a bannedlist id """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT MAX(ub_id) FROM user_bannedlist")
    result = cur.fetchone()
    con.close()
    if result[0] is None:
        ub_id = "ub" + "1".zfill(7)
    else:
        num = int(result[0].strip("ub")) + 1
        ub_id = "ub" + str(num).zfill(7)
    return ub_id


def check_is_in_banned_list(u_id, banned_u_id):
    """ Check is the user already in the bannedlist """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("""
        SELECT count(*)
        FROM user_bannedlist a
        WHERE a.u_id = "{}"
        AND a.banned_u_id = "{}"
    """.format(u_id, banned_u_id))
    result = cur.fetchone()
    if result[0] > 0:
        return True
    else:
        return False


def is_password_valid(password):
    """
    Return false if password entered is less than 6 characters long
    return true if password is valid
    """
    return bool((len(password) >= 6) & (len(password) <= 16))


def is_email_valid(email):
    """
    Return false if email entered is not a valid email
    return true if vaild
    """
    # | regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$" <- 不支持学校邮箱
    # v 换成下面这个
    regex = r"^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(?:\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$"
    return not bool(re.match(regex, email) is None)


def is_email_used(email):
    """
    Return true if email address is already being used by another user
    otherwise return false
    """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT u_email FROM web_user where u_email = ?"), (email,))
    result = cur.fetchone()
    con.close()
    if result is not None:
        return True
    return False


def is_username_in_range(username):
    """
    username is between 5 and 30 characters in length
    return true if in range
    """
    return bool(len(username) in range(5, 30))


def is_username_used(username):
    """
    Return true if username is already being used by another user
    otherwise return false
    """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(
        ("SELECT u_username FROM web_user where u_username = ?"), (username,))
    result = cur.fetchone()
    con.close()
    if result is not None:
        return True
    return False


def is_password_correct(email, password):
    """
    Return true if the password matches the password in the database
    """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT u_password FROM web_user where u_email = ?"), (email,))
    result = cur.fetchone()[0]
    con.close()
    if result == generate_password(password):
        return True
    return False


def is_token_valid(token):
    """
    Check wether is token valid
    return trun if valid
    """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT u_token FROM web_user where u_token = ?"), (token,))
    result = cur.fetchone()
    con.close()
    if result is not None:
        return True
    return False


def is_user_id_valid(u_id):
    """
    Return true if user id matches any user id in the database
    """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT u_token FROM web_user where u_id = ?"), (u_id,))
    result = cur.fetchone()
    con.close()
    if result is not None:
        return True
    return False


def check_reset_code(reset_code):
    """ check the reset code from the user matches the reset code in the database """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT * FROM web_user where u_reset_code = ?"), (reset_code,))
    result = cur.fetchone()
    con.close()
    if result is not None:
        return True
    return False


def get_info_from_reset(reset_code):
    """ get user infomation from reset code """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT u_token FROM web_user where u_reset_code = ?"), (reset_code,))
    result = cur.fetchone()
    con.close()
    return result


def is_name_in_range(name):
    """
    first name and last name not is between 1 and 50 characters in length
    return true if in range
    """
    return bool((len(name) in range(1, 51)))


def is_message_id_valid(ms_id):
    """ check is the given message id valid """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT ms_id FROM message_list where ms_id = '{}'".format(ms_id))
    result = cur.fetchone()
    con.close()
    if result is None:
        return False
    return True


def is_user_email_verify(token):
    """ check is the email from the given user is none or not """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT u_is_verify FROM web_user where u_token = '{}'".format(token))
    result = cur.fetchone()[0]
    con.close()
    return convert_int_to_boolean(result)

def is_email_used_temp_data(email):
    """ check is the email being used in the temporary data """
    for user in USER_DATA:
        if user.get('u_email') == email:
            return True
    return False


def is_username_used_temp_data(username):
    """ check is the username being used in the temporary data """
    for user in USER_DATA:
        if user.get('u_username') == username:
            return True
    return False


def append_temp_user(user_dict):
    """ append the given user_dict into temporary data """
    USER_DATA.append(user_dict)


def delete_temp_user_detail(u_id):
    """ delete the given user_dict from temporary data by the u_id """
    USER_DATA[:] = [i for i in USER_DATA if not (i['u_id'] == u_id)]


def get_user_info(u_id):
    """ get the user information by the given u_id """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("""
        SELECT u_id, u_username, u_email, u_avatar,
        u_lastname, u_firstname, u_is_critic_reviewer
        FROM web_user where u_id = '{}'
    """.format(u_id))
    result = cur.fetchone()
    con.close()
    u_is_critic_reviewer = convert_int_to_boolean(result[6])
    user_dict = {
        "u_id": result[0],
        "u_username": result[1],
        "u_email": result[2],
        "u_avatar": result[3],
        "u_lastname": result[4],
        "u_firstname": result[5],
        "u_is_critic_reviewer": u_is_critic_reviewer,
    }
    return user_dict


def get_uid(token):
    """ get the user id by the given token """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT u_id FROM web_user where u_token = '{}'".format(token))
    result = cur.fetchone()
    con.close()
    return result[0]


def convert_int_to_boolean(integer):
    """ convert the given integer to boolean """
    if integer == 0:
        return False
    else:
        return True
