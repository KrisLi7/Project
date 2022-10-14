"""
Implementation for person_details.py
person is referred to the movie's cast, director, producer or writer
"""

import sqlite3

import movie.movie_details as MovieDetails
import movie.movie_util as MovieUtil
from error import AccessError


def getMovieDetail(film_list, table, p_id):
    """
    A helper function for get_person_detail()
    that used to get all the movie detail that the
    person has contributed to.
    """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT m_id FROM '{}' WHERE p_id = '{}'".format(table, p_id))
    result = cur.fetchall()
    con.close()
    for m_id in result:
        movie_dict = MovieDetails.movie_details(m_id[0])
        if movie_dict not in film_list:
            film_list.append(movie_dict)


def get_person_detail(p_id):
    """
    Given a p_id, then return the corresponding person's details

    Args:
        p_id: A string of the person's id

    Returns:
        A dictionary that contain all the person's detail

    Raises:
        AccessError("Invalid person"):
            the input p_id does not match any p_id in the database
    """
    if not MovieUtil.is_person_exist(p_id):
        raise AccessError("Invalid person")

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT * From web_person where p_id = ?"), (p_id,))
    result = cur.fetchone()
    con.close()

    p_biography = result[5]
    if len(p_biography) >= 1500:
        p_bio_expand = True
        p_biography = p_biography[0:1500] + " ...."
    else:
        p_bio_expand = False

    person_dict = {
        'p_id': p_id,
        'p_name': result[1],
        "p_birth_name": result[2],
        "p_nick_name": result[3],
        "p_akas": result[4],
        'p_biography': p_biography,
        "p_birth_info": result[6],
        "p_birth_date": result[7],
        'p_headshot': result[8],
        'p_height': result[9],
        'p_bio_expand': p_bio_expand,
    }

    filmography_list = []
    getMovieDetail(filmography_list, "movie_director", p_id)
    getMovieDetail(filmography_list, "movie_producer", p_id)
    getMovieDetail(filmography_list, "movie_writer", p_id)
    getMovieDetail(filmography_list, "movie_cast", p_id)
    filmography_list.sort(key=lambda key: key['m_imdb_rate'], reverse=True)
    person_dict["p_filmography"] = filmography_list

    return person_dict

def expand_biography(p_id):
    """
    Given a p_id, then return the full biography for this person

    Args:
        p_id: A string of the person's id

    Returns:
        A dictionary that contains the full biography

    Raises:
        AccessError("Invalid person"):
            the input p_id does not match any p_id in the database
    """
    if not MovieUtil.is_person_exist(p_id):
        raise AccessError("Invalid person")

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT p_biography From web_person WHERE p_id = ?"), (p_id,))
    result = cur.fetchone()
    con.close()

    return {
        'p_biography': result[0]
    }