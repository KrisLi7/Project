"""
Implementation for movie_details.py
"""
import sqlite3
from error import AccessError
import movie.movie_util as MovieUtil
import movie.movie_details as MovieDetails


def movie_details(m_id: str):
    """
    Give the m_id for a certain movie
    and return the detail information about this m_id

    Args:
        m_id: A string of movie id

    Returns:
        A dictionary that contain the information including:
        m_id, m_title, m_info, m_poster, m_imdb_rate, m_year, m_language
        m_country, m_web_rate, m_genre, m_star, m_cast, m_director, m_critic_web_rate

    Raises:
        AccessError("Invalid movie")
            the movie with m_id not exist in database
    """

    if not MovieUtil.is_movie_exist(m_id):
        raise AccessError("Invalid movie")

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(
        ("SELECT m_title, m_info, m_poster, m_rating, m_year From web_movie where m_id = ?"), (m_id,))
    result = cur.fetchone()
    movie_dict = {
        'm_id': m_id,
        'm_title': result[0],
        'm_info': result[1],
        'm_poster': result[2],
        'm_imdb_rate': result[3],
        'm_year': result[4],
    }

    cur.execute(
        ("SELECT a.la_name FROM web_language a, movie_language b WHERE a.la_id = b.la_id AND b.m_id = ?"), (m_id,))
    result = cur.fetchone()
    if result is None:
        movie_dict['m_language'] = ""
    else:
        movie_dict['m_language'] = result[0]

    cur.execute(
        ("SELECT a.c_name FROM web_country a, movie_Country b WHERE a.c_id = b.c_id AND b.m_id = ?"), (m_id,))
    result = cur.fetchone()
    if result is None:
        movie_dict['m_country'] = ""
    else:
        movie_dict['m_country'] = result[0]
    movie_dict['m_web_rate'] = 0

    cur.execute(
        ("SELECT a.g_name FROM web_genre a, movie_genre b WHERE a.g_id = b.g_id AND b.m_id = ?"), (m_id,))
    result = cur.fetchone()
    if result is None:
        movie_dict['m_genre'] = ""
    else:
        movie_dict['m_genre'] = result[0]

    cast_list = []
    star_list = []
    cur.execute(("""SELECT a.p_id, a.p_name, b.role, b.is_star, a.p_headshot
                    FROM web_person a, movie_cast b
                    WHERE a.p_id = b.p_id
                    AND b.m_id = ?"""), (m_id,))

    for result in cur.fetchall():
        person_info = [result[0], result[1], result[2], result[4]]
        if result[3] == 1:
            star_list.append(person_info)
        else:
            cast_list.append(person_info)

    movie_dict['m_star'] = star_list
    movie_dict['m_cast'] = cast_list

    director_list = []
    cur.execute(("""SELECT a.p_id, a.p_name
                    FROM web_person a, movie_director b
                    WHERE a.p_id = b.p_id
                    AND b.m_id = ?
                    ORDER BY a.p_name"""), (m_id,))

    for result in cur.fetchall():
        person_info = [result[0], result[1]]
        director_list.append(person_info)
    movie_dict['m_director'] = director_list
    movie_dict['m_web_rate'] = get_average(m_id)
    movie_dict['m_critic_web_rate'] = get_average_critic(m_id)
    movie_dict['m_similar'] = get_similar(movie_dict)
    con.close()

    return movie_dict


def get_average(m_id):
    """help function to calculate the average rate of movie with m_id"""
    if not MovieUtil.is_movie_exist(m_id):
        raise AccessError("Invalid movie")
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    query = """
            SELECT count(*) 
            FROM web_movie_review wmr
            WHERE wmr.m_id = "{}"
        """.format(m_id)

    cur.execute(query)
    result = cur.fetchone()
    count = result[0]

    query = """
            SELECT wmr.r_rate
            FROM web_movie_review wmr
            WHERE wmr.m_id = "{}"
        """.format(m_id)
    cur.execute(query)

    total_rate = 0
    for result in cur.fetchall():
        total_rate = total_rate + result[0]
    if total_rate != 0:
        average_rate = total_rate / count
    else:
        average_rate = 0

    con.close()
    return round(average_rate, 1)


def get_average_critic(m_id):
    """ help function to calculate the average rate of movie with m_id from critic reviewers"""
    if not MovieUtil.is_movie_exist(m_id):
        raise AccessError("Invalid movie")
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    query = """
            SELECT count(*) 
            FROM web_movie_review wmr, web_user wu
            WHERE wmr.m_id = "{}"
            AND wu.u_is_critic_reviewer = 1
            AND wu.u_id = wmr.u_id
        """.format(m_id)

    cur.execute(query)
    result = cur.fetchone()
    count = result[0]

    query = """
            SELECT wmr.r_rate
            FROM web_movie_review wmr, web_user wu
            WHERE wmr.m_id = "{}"
            AND wu.u_is_critic_reviewer = 1
            AND wu.u_id = wmr.u_id
        """.format(m_id)
    cur.execute(query)

    total_rate = 0
    for result in cur.fetchall():
        total_rate = total_rate + result[0]
    if total_rate != 0:
        average_rate = total_rate / count
    else:
        average_rate = 0

    con.close()
    return round(average_rate, 1)


def get_similar(movie_dict):
    """help function for get similar movies"""
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()

    movie_genre = movie_dict['m_genre']
    movie_genres = movie_genre.split(", ")
    similar_movies = []

    for curr_director in movie_dict['m_director']:
        if len(similar_movies) >= 3:
            break
        curr_id = curr_director[0]
        query = """SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating
                     FROM web_movie a, movie_director b, web_person c
                     WHERE a.m_id = b.m_id
                     AND b.p_id = c.p_id
                     AND UPPER(c.p_id) = UPPER("{}")
                     AND a.m_id != "{}"
                     ORDER BY a.m_rating DESC, a.m_title
                         """.format(curr_id, movie_dict["m_id"])

        cur.execute(query)
        for result in cur.fetchall():
            average = MovieDetails.get_average(result[0])
            s_movie_dict = {
                "m_id": result[0],
                "m_title": result[1],
                "m_poster": result[2],
                "m_imdb_rate": result[3],
                "m_web_rate": average
            }

            if s_movie_dict not in similar_movies:
                similar_movies.append(s_movie_dict)
            if len(similar_movies) >= 3:
                break

    query = """ SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating
                 FROM web_movie a, movie_genre b, web_genre c
                 WHERE a.m_id = b.m_id
                 AND b.g_id = c.g_id
                 AND UPPER(c.g_name) like UPPER("%{}%")
                 AND a.m_id != "{}"
                 INTERSECT
                 SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating
                 FROM web_movie a
                 WHERE UPPER(a.m_title) like UPPER("%{}%")
                 AND a.m_id != "{}"
                 ORDER BY a.m_rating DESC, a.m_title
                 """.format(movie_genre, movie_dict["m_id"], movie_dict["m_title"], movie_dict["m_id"])
    cur.execute(query)
    for result in cur.fetchall():
        average = MovieDetails.get_average(result[0])
        s_movie_dict = {
            "m_id": result[0],
            "m_title": result[1],
            "m_poster": result[2],
            "m_imdb_rate": result[3],
            "m_web_rate": average
        }
        if s_movie_dict not in similar_movies:
            similar_movies.append(s_movie_dict)
        if len(similar_movies) >= 9:
            break

    if len(similar_movies) < 9:
        query = """ SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating
                         FROM web_movie a, movie_genre b, web_genre c
                         WHERE a.m_id = b.m_id
                         AND b.g_id = c.g_id
                         AND UPPER(c.g_name) = UPPER("{}")
                         AND a.m_id != "{}"
                         ORDER BY a.m_rating DESC, a.m_title
                 """.format(movie_genre, movie_dict["m_id"])

    cur.execute(query)
    for result in cur.fetchall():
        average = MovieDetails.get_average(result[0])
        s_movie_dict = {
            "m_id": result[0],
            "m_title": result[1],
            "m_poster": result[2],
            "m_imdb_rate": result[3],
            "m_web_rate": average
        }
        if s_movie_dict not in similar_movies:
            similar_movies.append(s_movie_dict)
        if len(similar_movies) >= 9:
            break

    if len(similar_movies) < 9:
        query = """ SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating
                         FROM web_movie a, movie_genre b, web_genre c
                         WHERE a.m_id = b.m_id
                         AND b.g_id = c.g_id
                         AND UPPER(c.g_name) like UPPER("%{}%")
                         AND a.m_id != "{}"
                         ORDER BY a.m_rating DESC, a.m_title
                 """.format(movie_genre, movie_dict["m_id"])

    cur.execute(query)
    for result in cur.fetchall():
        average = MovieDetails.get_average(result[0])
        s_movie_dict = {
            "m_id": result[0],
            "m_title": result[1],
            "m_poster": result[2],
            "m_imdb_rate": result[3],
            "m_web_rate": average
        }
        if s_movie_dict not in similar_movies:
            similar_movies.append(s_movie_dict)
        if len(similar_movies) >= 9:
            break

    for curr_genre in movie_genres:
        if len(similar_movies) >= 9:
            break
        query = """SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating
                                 FROM web_movie a, movie_genre b, web_genre c
                                 WHERE a.m_id = b.m_id
                                 AND b.g_id = c.g_id
                                 AND UPPER(c.g_name) like UPPER("%{}%")
                                 AND a.m_id != "{}"
                                 ORDER BY a.m_rating DESC, a.m_title
                         """.format(curr_genre, movie_dict["m_id"])
        cur.execute(query)
        for result in cur.fetchall():
            average = MovieDetails.get_average(result[0])
            s_movie_dict = {
                "m_id": result[0],
                "m_title": result[1],
                "m_poster": result[2],
                "m_imdb_rate": result[3],
                "m_web_rate": average
            }

            if s_movie_dict not in similar_movies:
                similar_movies.append(s_movie_dict)
            if len(similar_movies) >= 9:
                break
    con.close()
    return similar_movies
