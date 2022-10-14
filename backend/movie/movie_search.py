"""
Implementation for movie_search.py
"""
import sqlite3
from error import InputError
import movie.movie_util as MovieUtil
import movie.movie_details as MovieDetails


def movie_search(key_word):
    """
    Given a keyword, then return all the movie that is related to the keyword

    Args:
        key_word: A string of the keyword

    Returns:
        A dictionary that contain a list of movie with its information
        search_dict = {
                "items": [{}]
            }

    Raises:
        InputError('Please input keyword'):
            the input key_word is empty
    """
    if len(key_word) == 0:
        raise InputError('Please input keyword')

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    search_dict = {}

    cur.execute("""SELECT distinct m_id, m_title, m_poster, m_rating, m_year
                   FROM web_movie
                   WHERE UPPER(m_title) like UPPER("%{}%")
                   ORDER BY m_rating DESC""".format(key_word))
    item_list = []
    for result in cur.fetchall():
        if len(item_list) > 100:
            break
        average = MovieDetails.get_average(result[0])
        result_dict = {
            "m_id": result[0],
            "m_title": result[1],
            "m_poster": result[2],
            "m_imdb_rate": result[3],
            "m_year": result[4],
            "m_web_rate": average
        }
        if MovieUtil.is_movie_in_list(result_dict, item_list):
            item_list.append(result_dict)

    cur.execute("""SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating, a.m_year
                       FROM web_movie a, movie_cast b, web_person c
                       WHERE a.m_id = b.m_id
                       AND b.p_id = c.p_id
                       AND UPPER(c.p_name) like UPPER("%{}%")
                       ORDER BY a.m_rating DESC, a.m_title""".format(key_word))
    for result in cur.fetchall():
        if len(item_list) > 100:
            break
        average = MovieDetails.get_average(result[0])
        result_dict = {
            "m_id": result[0],
            "m_title": result[1],
            "m_poster": result[2],
            "m_imdb_rate": result[3],
            "m_year": result[4],
            "m_web_rate": average
        }
        if MovieUtil.is_movie_in_list(result_dict, item_list):
            item_list.append(result_dict)

    cur.execute("""SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating, a.m_year
                       FROM web_movie a, movie_director b, web_person c
                       WHERE a.m_id = b.m_id
                       AND b.p_id = c.p_id
                       AND UPPER(c.p_name) like UPPER("%{}%")
                       ORDER BY a.m_rating DESC, a.m_title""".format(key_word))
    for result in cur.fetchall():
        if len(item_list) > 100:
            break
        average = MovieDetails.get_average(result[0])
        result_dict = {
            "m_id": result[0],
            "m_title": result[1],
            "m_poster": result[2],
            "m_imdb_rate": result[3],
            "m_year": result[4],
            "m_web_rate": average
        }
        if MovieUtil.is_movie_in_list(result_dict, item_list):
            item_list.append(result_dict)

    cur.execute("""SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating, a.m_year
                       FROM web_movie a, movie_genre b, web_genre c
                       WHERE a.m_id = b.m_id
                       AND b.g_id = c.g_id
                       AND UPPER(c.g_name) like UPPER("%{}%")
                       ORDER BY a.m_rating DESC,a.m_title""".format(key_word))
    for result in cur.fetchall():
        if len(item_list) > 100:
            break
        average = MovieDetails.get_average(result[0])
        result_dict = {
            "m_id": result[0],
            "m_title": result[1],
            "m_poster": result[2],
            "m_imdb_rate": result[3],
            "m_year": result[4],
            "m_web_rate": average
        }
        if MovieUtil.is_movie_in_list(result_dict, item_list):
            item_list.append(result_dict)
    search_dict['items'] = item_list
    con.close()
    return search_dict


def movie_search_finity(key_word, num_show):
    """
    Given a keyword, then return only a specific number (depends on the given num_show)
    of movie that is related to the keyword

    Args:
        key_word: A string of the keyword
        num_show: A int that specified how many movie will be return

    Returns:
        A dictionary that contain a list of movie with its information
        search_dict = {
                "items": [{}]
            }

    Raises:
        InputError('Please input keyword'):
            the input key_word is empty
    """
    if key_word == "":
        raise InputError('Please input keyword')
    if num_show <= 0:
        raise  InputError('Please input number of result')

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    search_dict = {}

    cur.execute("""SELECT distinct (m_id), m_title, m_poster, a.m_rating, a.m_year
                   FROM web_movie
                   WHERE UPPER(m_title) like UPPER("%{}%")
                   ORDER BY a.m_rating DESC""".format(key_word))
    item_list = []
    for result in cur.fetchall():
        average = MovieDetails.get_average(result[0])
        result_dict = {
            "m_id": result[0],
            "m_title": result[1],
            "m_poster": result[2],
            "m_imdb_rate": result[3],
            "m_year": result[4],
            "m_web_rate": average
        }
        if MovieUtil.is_movie_in_list(result_dict, item_list):
            item_list.append(result_dict)
        if len(item_list) >= num_show:
            break

    if len(item_list) < num_show:
        cur.execute("""SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating, a.m_year
                           FROM web_movie a, movie_cast b, web_person c
                           WHERE a.m_id = b.m_id
                           AND b.p_id = c.p_id
                           AND UPPER(c.p_name) like UPPER("%{}%")
                           ORDER BY a.m_rating DESC, a.m_title""".format(key_word))
        for result in cur.fetchall():
            average = MovieDetails.get_average(result[0])
            result_dict = {
                "m_id": result[0],
                "m_title": result[1],
                "m_poster": result[2],
                "m_imdb_rate": result[3],
                "m_year": result[4],
                "m_web_rate": average
            }
            if MovieUtil.is_movie_in_list(result_dict, item_list):
                item_list.append(result_dict)
            if len(item_list) >= num_show:
                break

    if len(item_list) < num_show:
        cur.execute("""SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating, a.m_year
                           FROM web_movie a, movie_director b, web_person c
                           WHERE a.m_id = b.m_id
                           AND b.p_id = c.p_id
                           AND UPPER(c.p_name) like UPPER("%{}%")
                           ORDER BY a.m_rating DESC, a.m_title""".format(key_word))
        for result in cur.fetchall():
            average = MovieDetails.get_average(result[0])
            result_dict = {
                "m_id": result[0],
                "m_title": result[1],
                "m_poster": result[2],
                "m_imdb_rate": result[3],
                "m_year": result[4],
                "m_web_rate": average
            }
            if MovieUtil.is_movie_in_list(result_dict, item_list):
                item_list.append(result_dict)
            if len(item_list) >= num_show:
                break

    search_dict['items'] = item_list
    con.close()
    return search_dict
