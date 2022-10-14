"""
Implementation for movie_recommend.py
"""
import sqlite3
import movie.movie_util as MovieUtil
import movie.movie_details as MovieDetails
import user.user_util as UserUtil
from error import InputError, AccessError



def movie_recommend(u_id):
    """
    Give the u_id for a certain user
    and return the list of movies need to be recommended

    Args:
        u_id: A string of user id

    Returns:
        A list of movies information including:
        m_id, m_title, m_poster, m_imdb_rate, m_year

    Raises:

    """

    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    recommend_movies = []
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
                SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating, a.m_year
                FROM web_movie a, movie_genre b, web_genre c
                WHERE a.m_id = b.m_id
                AND b.g_id = c.g_id
                AND UPPER(c.g_name) like UPPER("%{}%")
                AND UPPER(c.g_name) like UPPER("%{}%")
                AND UPPER(c.g_name) not like UPPER("{}")
                ORDER BY a.m_rating DESC
        """.format(first_genre, second_genre, "short")
        cur.execute(query)
        for result in cur.fetchall():
            average = MovieDetails.get_average(result[0])
            movie_info = {
                "m_id": result[0],
                "m_title": result[1],
                "m_poster": result[2],
                "m_imdb_rate": result[3],
                "m_year": result[4],
                "m_web_rate": average,
            }
            
            if MovieUtil.is_movie_in_list(movie_info, recommend_movies):
                recommend_movies.append(movie_info)
            if len(recommend_movies) >= 4:
                break

        query = """
                        SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating, a.m_year
                        FROM web_movie a, movie_genre b, web_genre c
                        WHERE a.m_id = b.m_id
                        AND b.g_id = c.g_id
                        AND UPPER(c.g_name) like UPPER("%{}%")
                        AND UPPER(c.g_name) not like UPPER("{}")
                        AND a.m_year like "20%"
                        ORDER BY a.m_rating DESC
                """.format(first_genre, "short")
        cur.execute(query)
        for result in cur.fetchall():
            average = MovieDetails.get_average(result[0])
            movie_info = {
                "m_id": result[0],
                "m_title": result[1],
                "m_poster": result[2],
                "m_imdb_rate": result[3],
                "m_year": result[4],
                "m_web_rate": average,
            }
            if MovieUtil.is_movie_in_list(movie_info, recommend_movies):
                recommend_movies.append(movie_info)
            if len(recommend_movies) >= 7:
                break

        query = """
                        SELECT distinct a.m_id, a.m_title, a.m_poster, a.m_rating, a.m_year
                        FROM web_movie a, movie_genre b, web_genre c
                        WHERE a.m_id = b.m_id
                        AND b.g_id = c.g_id
                        AND UPPER(c.g_name) like UPPER("%{}%")
                        AND UPPER(c.g_name) not like UPPER("{}")
                        AND a.m_year like "20%"
                        ORDER BY a.m_rating DESC 
                """.format(second_genre, "short")
        cur.execute(query)
        for result in cur.fetchall():
            average = MovieDetails.get_average(result[0])
            movie_info = {
                "m_id": result[0],
                "m_title": result[1],
                "m_poster": result[2],
                "m_imdb_rate": result[3],
                "m_year": result[4],
                "m_web_rate": average,
            }
            if MovieUtil.is_movie_in_list(movie_info, recommend_movies):
                recommend_movies.append(movie_info)
            if len(recommend_movies) >= 9:
                break
    else:
        query = """
            SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
            FROM web_movie_review wmr, web_movie wm
            WHERE wmr.m_id = wm.m_id
            ORDER BY wm.m_rating DESC
        """
        cur.execute(query)
        for result in cur.fetchall():
            average = MovieDetails.get_average(result[0])
            movie_info = {
                "m_id": result[0],
                "m_title": result[1],
                "m_poster": result[2],
                "m_imdb_rate": result[3],
                "m_year": result[4],
                "m_web_rate": average,
            }
            if MovieUtil.is_movie_in_list(movie_info, recommend_movies):
                recommend_movies.append(movie_info)
            if len(recommend_movies) >= 9:
                break
        if len(recommend_movies) < 9:
            query = """
                SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                FROM web_movie wm
                WHERE wm.m_year = "{}"
                ORDER BY wm.m_rating DESC
            """.format("2022")
            cur.execute(query)
            for result in cur.fetchall():
                average = MovieDetails.get_average(result[0])
                movie_info = {
                    "m_id": result[0],
                    "m_title": result[1],
                    "m_poster": result[2],
                    "m_imdb_rate": result[3],
                    "m_year": result[4],
                    "m_web_rate": average,
                }
                if MovieUtil.is_movie_in_list(movie_info, recommend_movies):
                    recommend_movies.append(movie_info)
                if len(recommend_movies) >= 9:
                    break
    return recommend_movies


def get_favorite_genre(u_id):
    """Help function the get user's favorite genre"""
    if not UserUtil.is_user_id_valid(u_id):
        raise AccessError("Invalid user")

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
