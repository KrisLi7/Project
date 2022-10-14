"""
Implementation for movie_advanced_search.py
"""
import sqlite3
from error import InputError
import movie.movie_util as MovieUtil
import movie.movie_details as MovieDetails


def movie_advanced_search(title, actor, director, country, r18, year, genre):
    """
    Give the title actor director country r18 year genre keyword
    and return the advanced search result based on the keyword

    Args:
        title: A string of movie title keyword
        actor: A string of actor name keyword
        director: A string of director name keyword
        country: A string of country name keyword
        r18: A boolean of whether include r18 movie or not
        year: A string of year keyword
        genre: A string of genre keyword

    Returns:
        A dictionary that contain the list of dictionaries of movie information
        including: m_id, m_title, m_poster, m_imdb_rate

    Raises:
        InputError('Please input keyword')
            the keyword input is empty
    """

    if len(title) + len(actor) + len(director) + len(country) + len(year) + len(genre) < 1:
        raise InputError('Please input keyword')

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    search_dict = {}

    query = """ """
    if len(title) > 0:
        query = query + """SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating
        FROM web_movie a
        WHERE UPPER(a.m_title) like UPPER("%{}%")
        """.format(title)

    if len(actor) > 0:
        if len(query) > 1:
            query = query + """
            INTERSECT
            """
        query = query + """SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating
        FROM web_movie a, movie_cast b, web_person c
        WHERE a.m_id = b.m_id
        AND b.p_id = c.p_id
        AND UPPER(c.p_name) like UPPER("%{}%")
        """.format(actor)

    if len(director) > 0:
        if len(query) > 1:
            query = query + """
            INTERSECT
            """
        query = query + """SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating
        FROM web_movie a, movie_director b, web_person c
        WHERE a.m_id = b.m_id
        AND b.p_id = c.p_id
        AND UPPER(c.p_name) like UPPER("%{}%")
        """.format(director)

    if len(country) > 0:
        if country != "All":
            if len(query) > 1:
                query = query + """
                INTERSECT
                """
            query = query + """SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating
            FROM web_movie a, movie_country b, web_country c
            WHERE a.m_id = b.m_id
            AND b.c_id = c.c_id
            AND UPPER(c.c_name) like UPPER("%{}%")
            """.format(country)

    if len(year) > 0:
        if len(query) > 1:
            query = query + """
            INTERSECT
            """
        query = query + """SELECT distinct (m_id), m_title, m_poster, a.m_rating
        FROM web_movie a
        WHERE UPPER(a.m_year) like UPPER("%{}%")
        """.format(year)

    if genre != "All":
        if len(genre) > 0:
            if len(query) > 1:
                query = query + """
                INTERSECT
                """

            query = query + """SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating
            FROM web_movie a, movie_genre b, web_genre c
            WHERE a.m_id = b.m_id
            AND b.g_id = c.g_id
            AND UPPER(c.g_name) like UPPER("%{}%")""".format(genre)
    elif not r18:
        if len(query) > 1:
            query = query + """
            INTERSECT
            """

        query = query + """SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating
        FROM web_movie a, movie_genre b, web_genre c
        WHERE a.m_id = b.m_id
        AND b.g_id = c.g_id
        AND UPPER(c.g_name) Not like UPPER("%{}%")""".format("Adult")
    else:
        if len(query) > 1:
            query = query + """
            INTERSECT
            """
        query = query + """ SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating
                FROM web_movie a """

    if len(query) > 1:
        query = query + """
        ORDER BY a.m_rating DESC
        """
    item_list = []
    cur.execute(query)
    for result in cur.fetchall():
        if len(item_list) > 100:
            break
        average = MovieDetails.get_average(result[0])
        result_dict = {
            "m_id": result[0],
            "m_title": result[1],
            "m_poster": result[2],
            "m_imdb_rate": result[3],
            "m_web_rate": average,
        }
        if MovieUtil.is_movie_in_list(result_dict, item_list):
            item_list.append(result_dict)
    search_dict['items'] = item_list
    con.close()
    return search_dict
