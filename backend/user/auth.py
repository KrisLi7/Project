""" Implementation for auth.py """

import sqlite3
import random
import string

from threading import Timer
from user.email import Email
import user.user_util as UserUtil
from error import InputError, AccessError

from memory.authData import USER_DATA


class Authorise:
    def __init__(self, time_data_store):
        self.cur_u_id = 0
        self.time_data_store = time_data_store


    def clear_all_user_data(self):
        """ A function that clean all user in the database """
        con = sqlite3.connect('data/db.sqlite3')
        cur = con.cursor()
        cur.execute("DELETE FROM web_user")
        cur.execute("DELETE FROM user_wishlist")
        cur.execute("DELETE FROM user_bannedlist")
        cur.execute("DELETE FROM message_list")
        con.commit()
        con.close()
        USER_DATA.clear()


    def temp_auth_register(self, username, email, password):
        """
        Given a user's username, email address, and password,
        create a new account for them in the temporary data,
        then send them a email verification

        Args:
            username: A string of username
            email: A string of email
            password: A string of password

        Returns:
            A dictionary that contain u_id, u_email, u_password and u_token

        Raises:
            InputError("Used email"):
                the given email is used by other user
            InputError("Invalid email"):
                the given email is not in the correct format
            InputError("Invalid password"):
                the given password is not in the correct format
            InputError("Invalid user name"):
                the given username is not in the correct format
            InputError("Used username"):
                the given username is used by other user
        """
        if UserUtil.is_email_used(email):
            raise InputError("Used email")
        if UserUtil.is_email_used_temp_data(email):
            raise InputError("Used email")
        if not UserUtil.is_email_valid(email):
            raise InputError("Invalid email")
        if not UserUtil.is_password_valid(password):
            raise InputError("Invalid password")
        if not UserUtil.is_username_in_range(username):
            raise InputError("Invalid username")
        if UserUtil.is_username_used(username):
            raise InputError("Used username")
        if UserUtil.is_username_used_temp_data(username):
            raise InputError("Used username")

        token = UserUtil.generate_token(username, email)
        encrypt_password = UserUtil.generate_password(password)
        if len(USER_DATA) != 0:
            self.cur_u_id += 1
            u_id = "us" + str(self.cur_u_id).zfill(7)
        else:
            con = sqlite3.connect('data/db.sqlite3')
            cur = con.cursor()
            cur.execute("SELECT COUNT(u_id) FROM web_user")
            self.cur_u_id = cur.fetchone()[0] + 1
            con.close()
            u_id = "us" + str(self.cur_u_id).zfill(7)

        user_dict = {
            "u_id": u_id,
            "u_email": email,
            "u_username": username,
            "u_token": token,
            "u_password": encrypt_password,
        }
        USER_DATA.append(user_dict)
        delete_later = Timer(self.time_data_store, UserUtil.delete_temp_user_detail, (u_id,))
        delete_later.start()

        send_later = Timer(1, Email(email, username).sendVerifyEmail, (u_id,))
        send_later.start()
        return {
            'u_id': u_id,
            "u_email": email,
            'u_username': username,
            'u_token': token,
        }


    def verify_email(self, u_id):
        """
        A function they verify the user's email address
        by check if the given u_id exist in the temporary data,
        the data in the temporary data will be deleted and all related
        info will be copy to the database

        Args:
            u_id: A string of user id

        Returns:
            A dictionary that contain u_id and u_email

        Raises:
            AccessError("Verfied fail, account is not exist in the system"):
                the given u_id does not exist in the temporary data
        """
        if not any(user.get('u_id') == u_id for user in USER_DATA):
            raise AccessError("Verfied fail, account is not exist in the system")

        for user in USER_DATA:
            if user.get('u_id') == u_id:
                user_dict = user

        con = sqlite3.connect('data/db.sqlite3')
        cur = con.cursor()
        if UserUtil.is_user_id_valid(u_id):
            query = "UPDATE web_user SET u_is_verify = 1 where u_id = '{}'".format(u_id)
            cur.execute(query)
        else:
            query = """
                INSERT INTO web_user(u_id, u_username, u_email, u_password,
                u_token, u_level, u_exp, u_is_critic_reviewer, u_is_login, u_notification, u_is_verify)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cur.execute(query, (u_id, user_dict.get("u_username"), user_dict.get("u_email"),
                user_dict.get("u_password"), user_dict.get("u_token"), 1, 0, 0, 0, 1, 1))
        con.commit()
        con.close()
        UserUtil.delete_temp_user_detail(u_id)

        return {
            'u_id': u_id,
            "u_email": user_dict.get("u_email"),
        }


    def auth_login(self, email, password):
        """
        Given a registered users' email and password
        and return a valid token for the user to remain authenticated

        Args:
            email:A string of email of the user
            password: A string of password of the user

        Returns:
            A dictionary with user's u_id and token who login

            {'u_id': i.get("u_id"),
            'token': i.get("token"),}

        Raises:
            InputError("Invalid Email"):
                the input email is invalid
            InputError("Not Belong To A User"):
                the email entered not belong to a user
        """
        if not UserUtil.is_email_valid(email):
            raise InputError("Invalid email")
        if not UserUtil.is_email_used(email):
            raise InputError("Not belong to a user")
        if not UserUtil.is_password_correct(email, password):
            raise InputError("Incorrect password")

        con = sqlite3.connect('data/db.sqlite3')
        cur = con.cursor()
        cur.execute(
            ("UPDATE web_user SET u_is_login = 1 where u_email = ?"), (email,))
        con.commit()

        cur.execute(
            ("SELECT * FROM web_user where u_email = ?"), (email,))
        result = cur.fetchone()
        login_dict = {
            'u_id': result[0],
            'u_username': result[2],
            'u_token': result[1],
            'u_is_login': result[11],
        }
        con.close()
        return login_dict


    def auth_logout(self, token):
        """
        Given an active token, invalidates the token to log the user out.
        If a valid token is given, and the user is successfully logged out,

        Args:
            token: A string used to identify a user.

        Returns:
            A dictionary that contains a success message

        Raises:
            AccessError("Invalid user"):
                The given token does not match any user in the database
        """
        if not UserUtil.is_token_valid(token):
            raise AccessError("Invalid user")

        con = sqlite3.connect('data/db.sqlite3')
        cur = con.cursor()
        cur.execute(("UPDATE web_user SET u_is_login = 0 where u_token = ?"), (token,))
        con.commit()
        con.close()
        return {'is_success': True}


    def auth_passwordreset_request(self, email):
        """
        Given an email address, if the user is a registered user, sends an
        email containing a specific secret code, so when the user entered the secret_code
        it will allow the user to change the password

        Args:
            email: A string of email address

        Returns:
            A dictionary that contains a reset code

        Raises:
            InputError("Not belong to a user")
                The given email does not match any user in the database
        """
        if not UserUtil.is_email_used(email):
            raise InputError("Not belong to a user")

        reset_code = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))
        while UserUtil.check_reset_code(reset_code):
            reset_code = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))

        con = sqlite3.connect('data/db.sqlite3')
        cur = con.cursor()
        cur.execute(("UPDATE web_user SET u_reset_code = ? where u_email = ?"), (reset_code, email))
        con.commit()
        cur.execute("Select u_username FROM web_user WHERE u_email = ?", (email,))
        username = cur.fetchone()[0]
        con.close()
        send_later = Timer(1, Email(email, username).sendResetEmail, (reset_code,))
        send_later.start()

        return {'reset_code': reset_code}


    def auth_password_reset(self, reset_code, new_password):
        """
        Given a reset code, if it match the reset code stored in the database,
        then it will change the user's password to the new given password

        Args:
            reset_code: A string of reset code
            new_password: A string of new password

        Returns:
            A dictionary that contains a success message

        Raises:
            InputError("Invalid reset code"):
                the given reset code does not matches the reset code stored in the database
            InputError("Invalid password"):
                the given password is not in the correct format
        """
        if not UserUtil.check_reset_code(reset_code):
            raise InputError("Invalid reset code")
        if not UserUtil.is_password_valid(new_password):
            raise InputError("Invalid password")

        user_info = UserUtil.get_info_from_reset(reset_code)
        new_password = UserUtil.generate_password(new_password)

        con = sqlite3.connect('data/db.sqlite3')
        cur = con.cursor()
        cur.execute(("UPDATE web_user SET u_reset_code = NULL where u_token = ?"), (user_info[0],))
        cur.execute(("UPDATE web_user SET u_password = ? where u_token = ?"), (new_password, user_info[0]))
        con.commit()
        con.close()
        return {'is_success': True}
