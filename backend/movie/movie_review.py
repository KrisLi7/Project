""" Implementation for movie_review.py """

import sqlite3

import user.user_util as UserUtil
import user.user_level as Level
import user.user_message as Message
import movie.movie_util as MovieUtil
from error import InputError, AccessError


def clean_all_review():
    """ A function that clean all review in the database """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("DELETE FROM web_movie_review")
    cur.execute("DELETE FROM review_react")
    con.commit()
    con.close()


def post_review(token, m_id, review, rate):
    """
    A function that will store the given variable into the table web_movie_review
    so that the review that's post by the user will be stored

    Args:
        token: A string used to identify a user
        m_id: A string of a movie id
        review: A string of review post by the user
        rate: The rating range from 0 to 5 as double

    Returns:
        A dictionary that contain the r_id (review id)

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
        AccessError("Please verify your email"):
            the given user has not verify their email after they request to change email
        InputError("Review is too long"):
            the input review is too long
        AccessError("Invalid movie"):
            the given movie id is not exist in the database
        InputError("Invalid rating"):
            The given rating is not in range from 0 to 5
    """
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    if not UserUtil.is_user_email_verify(token):
        raise AccessError("Please verify your email")
    if len(review) > 5000:
        raise InputError("Review is too long")
    if not MovieUtil.is_movie_exist(m_id):
        raise AccessError("Invalid movie")
    if not MovieUtil.is_rate_valid(rate):
        raise InputError("Invalid rating")

    u_id = UserUtil.get_uid(token)
    u_username = UserUtil.get_user_info(u_id).get("u_username")
    time_created = MovieUtil.unix_datetime()
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT COUNT(r_id) FROM web_movie_review")
    r_id = "re" + str(cur.fetchone()[0] + 1).zfill(7)
    query = "INSERT INTO web_movie_review(r_id, m_id, u_id, r_rate, r_review, r_time_created) VALUES (?, ?, ?, ?, ?, ?)"
    cur.execute(query, (r_id, m_id, u_id, rate,
                        review, time_created))
    con.commit()
    con.close()

    Level.alter_exp(u_id, 100)
    Message.check_mess_send_to_which_us(m_id, u_id, u_username)
    return {
        'r_id': r_id,
    }


def get_movie_review(token, m_id):
    """
    A function that get all the review in our database
    If a token is provided, then the review from the user who got banned
    by the given user (user that matches the token) wil not be included

    Args:
        token: A string used to identify a user
        m_id: A string of a movie id

    Returns:
        A list of dictionary that contain the review details
        review_list = [{review}, {review}]

    Raises:
        AccessError("Invalid movie"):
            the given movie id is not exist in the database
        AccessError("Invalid user"):
            the given token does not match any user in the database
    """
    if not MovieUtil.is_movie_exist(m_id):
        raise AccessError("Invalid movie")

    review_list = []
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("""
        SELECT wmr.r_id, wmr.m_id, wmr.u_id,
        wmr.r_rate, wmr.r_review, wmr.r_time_created
        FROM web_movie_review wmr
        JOIN web_user wu ON wmr.u_id = wu.u_id
        WHERE m_id = '{}'
        ORDER BY wu.u_is_critic_reviewer DESC, r_time_created DESC
    """.format(m_id))
    results = cur.fetchall()
    con.close()
    if len(token) == 0:
        get_all_movie_review(review_list, results)
    else:
        u_id = UserUtil.get_uid(token)
        if not UserUtil.is_token_valid(token):
            raise AccessError("Invalid user")
        get_movie_review_from_unbanned_user(review_list, results, u_id)
    return review_list


def get_all_movie_review(review_list, data):
    """
    A helper function that will be called by get_movie_review()
    when the token is not provided.
    Simply get all the review exist in the database
    """
    for review in data:
        profile = UserUtil.get_user_info(review[2])
        r_like = MovieUtil.count_like_react(review[0])
        r_dislike = MovieUtil.count_dislike_react(review[0])
        review_dict = {
            "r_id": review[0],
            "u_id": profile.get('u_id'),
            "u_username": profile.get('u_username'),
            "u_is_critic_reviewer": profile.get('u_is_critic_reviewer'),
            "u_avatar": profile.get('u_avatar'),
            "r_rate": review[3],
            "r_review": review[4],
            "r_time_created": review[5],
            "r_like": r_like,
            "r_dislike": r_dislike,
            "r_is_like": False,
            "r_is_dislike": False
        }
        review_list.append(review_dict)


def get_movie_review_from_unbanned_user(review_list, data, u_id):
    """
    A helper function that will be called by get_movie_review()
    when the token is provided.
    Review from the banned user will not be included
    """
    for review in data:
        if not UserUtil.check_is_in_banned_list(u_id, review[2]):
            profile = UserUtil.get_user_info(review[2])
            r_like = MovieUtil.count_like_react(review[0])
            r_dislike = MovieUtil.count_dislike_react(review[0])
            r_is_like = MovieUtil.check_is_user_react_like(review[0], u_id)
            r_is_dislike = MovieUtil.check_is_user_react_dislike(review[0], u_id)
            review_dict = {
                "r_id": review[0],
                "u_id": profile.get('u_id'),
                "u_username": profile.get('u_username'),
                "u_is_critic_reviewer": profile.get('u_is_critic_reviewer'),
                "u_avatar": profile.get('u_avatar'),
                "r_rate": review[3],
                "r_review": review[4],
                "r_time_created": review[5],
                "r_like": r_like,
                "r_dislike": r_dislike,
                "r_is_like": r_is_like,
                "r_is_dislike": r_is_dislike
            }
            review_list.append(review_dict)


def review_react(token, r_id, ra_id):
    """
    A function that stored the action of reacting like/dislike
    from the user on the given review into the database

    Args:
        token: A string used to identify a user
        r_id: A string of a review id
        ra_id: a string "1" (like) or "2" (dislike)

    Returns:
        A dict containg a message of success

    Raises:
        AccessError("Invalid user"):
            the given token does not match any user in the database
        AccessError("Please verify your email"):
            the given user has not verify their email after they request to change email
        AccessError("Invalid review"):
            the given review id is not exist in the database
        InputError("Invalid react action"):
            the given ra_id does not match any react in the database
    """
    ra_id = "ra" + ra_id.zfill(7)
    if not UserUtil.is_token_valid(token):
        raise AccessError("Invalid user")
    if not UserUtil.is_user_email_verify(token):
        raise AccessError("Please verify your email")
    if not MovieUtil.is_review_exist(r_id):
        raise AccessError("Invalid review")
    if not MovieUtil.is_react_exist(ra_id):
        raise InputError("Invalid react action")

    u_id = UserUtil.get_uid(token)
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    query = "SELECT ra_id FROM review_react WHERE u_id = ? AND r_id = ?"
    cur.execute(query, (u_id, r_id))
    old_ra_id = cur.fetchone()

    query = "SELECT u_id FROM web_movie_review WHERE r_id = '{}'".format(r_id)
    cur.execute(query)
    react_u_id = cur.fetchone()[0]
    con.close()
    if old_ra_id is None:
        MovieUtil.insert_review_react(u_id, r_id, ra_id)
        Level.check_increase_or_decrease_exp(react_u_id, ra_id)
    elif ra_id == old_ra_id[0]:
        MovieUtil.review_unreact(u_id, r_id)
        Level.revoke_exp(react_u_id, old_ra_id[0])
    else:
        MovieUtil.review_unreact(u_id, r_id)
        MovieUtil.insert_review_react(u_id, r_id, ra_id)
        Level.revoke_exp(react_u_id, old_ra_id[0])
        Level.check_increase_or_decrease_exp(react_u_id, ra_id)

    return {
        "is_success": True
    }
