""" Implementation for email_recommend.py """

import sqlite3

from threading import Timer
from datetime import datetime

from user.email import Email


def recommend_newly_release_movie():
    """
    A function that will send email recommendation of newly
    realease movie to user

    Returns:
            A dictionary that contain a success message
    """
    new_movie_list = []
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    query = """
        SELECT u_id, u_username, u_email from web_user
        WHERE u_notification = "1"
    """
    cur.execute(query)
    user_res = cur.fetchall()
    for user in user_res:
        new_movie_list = get_recommed_movies(user[0], date_string)
        if len(new_movie_list) > 0:
            send_later = Timer(1, Email(user[2], user[1]).sendRecommendEmail,
            (new_movie_list,))
            send_later.start()

    query = """
        DELETE from coming_soon_movie
        WHERE release_date <= "{}"
    """.format(date_string)
    cur.execute(query)
    con.commit()
    con.close()
    return {"is_success": True}


def get_recommed_movies(u_id, date_string):
    """
    A function that recommend movie to user by their wishlist
    or commented movie
    """
    new_movie_list = []
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    query = """
            SELECT distinct wmr.m_id
            FROM web_movie_review wmr
            WHERE wmr.u_id = "{}"
    """.format(u_id)
    watched_movies = []
    cur.execute(query)
    for result in cur.fetchall():
        watched_movies.append(result[0])

    if len(watched_movies) > 0:
        first_genre, second_genre = get_favorite_genre(u_id)

        query = """
            SELECT wm.m_id, wm.m_title, csm.release_date
            FROM coming_soon_movie csm, web_genre wg, movie_genre mg, web_movie wm
            WHERE csm.m_id = mg.m_id
            AND mg.g_id = wg.g_id
            AND wm.m_id = csm.m_id
            AND UPPER(wg.g_name) like UPPER("%{}%")
            AND UPPER(wg.g_name) like UPPER("%{}%")
            AND csm.release_date <= "{}"
        """.format(first_genre, second_genre, date_string)
        cur.execute(query)
        for result in cur.fetchall():
            movie_list = [result[0], result[1], result[2]]
            new_movie_list.append(movie_list)

        query = """
            SELECT wm.m_id, wm.m_title, csm.release_date
            FROM coming_soon_movie csm, web_genre wg, movie_genre mg, web_movie wm
            WHERE csm.m_id = mg.m_id
            AND wm.m_id = csm.m_id
            AND mg.g_id = wg.g_id
            AND UPPER(wg.g_name) like UPPER("%{}%")
            AND csm.release_date <= "{}"
        """.format(first_genre, date_string)
        cur.execute(query)
        for result in cur.fetchall():
            movie_list = [result[0], result[1], result[2]]
            if is_movie_in_list(movie_list, new_movie_list):
                new_movie_list.append(movie_list)

        query = """
            SELECT wm.m_id, wm.m_title, csm.release_date
            FROM coming_soon_movie csm, web_genre wg, movie_genre mg, web_movie wm
            WHERE csm.m_id = mg.m_id
            AND wm.m_id = csm.m_id
            AND mg.g_id = wg.g_id
            AND UPPER(wg.g_name) like UPPER("%{}%")
            AND csm.release_date <= "{}"
        """.format(second_genre, date_string)
        cur.execute(query)
        for result in cur.fetchall():
            movie_list = [result[0], result[1], result[2]]
            if is_movie_in_list(movie_list, new_movie_list):
                new_movie_list.append(movie_list)
    con.close()
    return new_movie_list


def get_favorite_genre(u_id):
    """
    A function that get user's favourite genre

    Returns:
            A string of genre
    """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    query = """
        SELECT wg.g_name
        From web_movie wm, web_genre wg, web_user wu, web_movie_review wmr, movie_genre mg
        WHERE wm.m_id = mg.m_id
        AND mg.g_id = wg.g_id
        AND wm.m_id = wmr.m_id
        AND wmr.u_id = "{}"
    """.format(u_id)
    cur.execute(query)
    all_genres = []
    for result in cur.fetchall():
        movie_genres = result[0].split(", ")
        all_genres.extend(movie_genres)

    query = """
        SELECT wg.g_name
        FROM web_genre wg, movie_genre mg, user_wishlist uw
        WHERE uw.u_id = "{}"
        AND uw.m_id = mg.m_id
        AND mg.g_id = wg.g_id
    """.format(u_id)
    cur.execute(query)
    for result in cur.fetchall():
        movie_genres = result[0].split(", ")
        all_genres.extend(movie_genres)
        all_genres.extend(movie_genres)
        all_genres.extend(movie_genres)

    first_genre = max(all_genres, key=all_genres.count)
    while first_genre in all_genres:
        all_genres.remove(first_genre)
    if len(all_genres) > 0:
        second_genre = max(all_genres, key=all_genres.count)
    else:
        second_genre = ""
    con.close()
    return first_genre, second_genre


def is_movie_in_list(result, list_dict):
    """ Check is the given movie list exist in the given movie list """
    for cur_list in list_dict:
        if cur_list[0] == result[0]:
            return False
    return True
