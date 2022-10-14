"""
Implementation for movie_homepage.py
"""
import sqlite3
import movie.movie_recommend as MovieRecommend
import movie.movie_util as MovieUtil
import movie.movie_details as MovieDetails


def movie_homepage(u_id):
    """
    Given the u_id for a certain user
    and return the movies need to placed on the homepage

    Args:
        u_id: A string of user id

    Returns:
        A dictionary that contain many lists of movies with information
        including: Items, Recommend, New, Action, Adventure, Comedy, Sci-fi, Crime
        each corresponding to a list of movies with their information

    Raises:

    """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(""" SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                    From web_movie wm, movie_genre b, web_genre c
                    where wm.m_rating < 10
                    AND wm.m_id = b.m_id
                    AND b.g_id = c.g_id
                    and wm.m_year = "2018"
                    AND UPPER(c.g_name) not like UPPER("%{}%")
                    ORDER BY wm.m_rating DESC """.format("short"))
    movie_dict = {}
    movie_list = []
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
        movie_list.append(result_dict)
        if len(movie_list) >= 9:
            break

    # top movies
    movie_dict['items'] = movie_list

    # Recommend
    movie_dict['Recommend'] = MovieRecommend.movie_recommend(u_id)

    # new movies
    new_list = []
    cur.execute(""" SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                    From web_movie wm, movie_genre b, web_genre c
                    where wm.m_rating < 10
                    AND wm.m_id = b.m_id
                    AND b.g_id = c.g_id
                    and wm.m_year = "2022"
                    And UPPER(c.g_name) not like UPPER("%{}%")
                    ORDER BY wm.m_rating DESC """.format("short"))
    for result in cur.fetchall():
        if len(new_list) >= 9:
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
        if result_dict['m_poster'] is not None:
            new_list.append(result_dict)

    movie_dict['New'] = new_list

    movie_dict['Action'] = action_movie()
    movie_dict['Adventure'] = adventure_movie()
    movie_dict['Comedy'] = comedy_movie()
    movie_dict['Sci-fi'] = sci_ci_movie()
    movie_dict['Crime'] = crime_movie()

    con.close()
    return movie_dict


def action_movie():
    """ help function for generate the action movies that need to be placed on homepage"""
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    # Action
    action_list = []
    # The Dark Knight
    cur.execute(""" SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                            From web_movie wm
                            where UPPER(wm.m_title) = UPPER("The Dark Knight") 
                            ORDER BY wm.m_rating DESC """)
    result = cur.fetchone()
    average = MovieDetails.get_average(result[0])
    result_dict = {
        "m_id": result[0],
        "m_title": result[1],
        "m_poster": result[2],
        "m_imdb_rate": result[3],
        "m_year": result[4],
        "m_web_rate": average
    }
    action_list.append(result_dict)
    # Kill Bill
    cur.execute(""" SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                            From web_movie wm
                            where UPPER(wm.m_title) like UPPER("%{}%") 
                            ORDER BY wm.m_rating DESC """.format("Kill Bill"))
    result = cur.fetchone()
    average = MovieDetails.get_average(result[0])
    result_dict = {
        "m_id": result[0],
        "m_title": result[1],
        "m_poster": result[2],
        "m_imdb_rate": result[3],
        "m_year": result[4],
        "m_web_rate": average
    }
    action_list.append(result_dict)

    # other action
    cur.execute(""" SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating, a.m_year
                        FROM web_movie a, movie_genre b, web_genre c
                        WHERE a.m_id = b.m_id
                        AND b.g_id = c.g_id
                        AND a.m_rating < 10
                        AND UPPER(c.g_name) like UPPER("%{}%") 
                        AND UPPER(c.g_name) not like UPPER("%{}%")
                        ORDER BY a.m_rating DESC """.format("Action", "Short"))

    for result in cur.fetchall():
        if len(action_list) >= 9:
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
        if MovieUtil.is_movie_in_list(result_dict, action_list) and result_dict['m_poster'] is not None:
            action_list.append(result_dict)

    con.close()
    return action_list


def adventure_movie():
    """ help function for generate the adventure movies that need to be placed on homepage"""
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    # Adventure
    # The Lord of the Rings
    adventure_list = []
    cur.execute(""" SELECT distinct (wm.m_id), wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                    From web_movie wm
                    where UPPER(wm.m_title) like UPPER("%{}%") 
                    ORDER BY wm.m_rating DESC """.format("The Lord of the Rings"))
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
        adventure_list.append(result_dict)
        if len(adventure_list) >= 9:
            break
    # other adventure
    cur.execute(""" SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating, a.m_year
                    FROM web_movie a, movie_genre b, web_genre c
                    WHERE a.m_id = b.m_id
                    AND b.g_id = c.g_id
                    AND UPPER(c.g_name) like UPPER("%{}%") 
                    AND UPPER(c.g_name) not like UPPER("%{}%")
                    ORDER BY a.m_rating DESC""".format("adventure", "Short"))

    for result in cur.fetchall():
        if len(adventure_list) >= 9:
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
        if MovieUtil.is_movie_in_list(result_dict, adventure_list) and result_dict['m_poster'] is not None:
            adventure_list.append(result_dict)
    con.close()
    return adventure_list


def comedy_movie():
    """ help function for generate the comedy movies that need to be placed on homepage"""
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    # Comedy
    comedy_list = []
    # Up
    cur.execute(""" SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                    From web_movie wm
                    where UPPER(wm.m_title) = UPPER("Up")
                    ORDER BY wm.m_rating DESC """)
    result = cur.fetchone()
    average = MovieDetails.get_average(result[0])
    result_dict = {
        "m_id": result[0],
        "m_title": result[1],
        "m_poster": result[2],
        "m_imdb_rate": result[3],
        "m_year": result[4],
        "m_web_rate": average
    }
    comedy_list.append(result_dict)

    # The Great Dictator
    cur.execute(""" SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                            From web_movie wm
                            where UPPER(wm.m_title) = UPPER("The Great Dictator")
                            ORDER BY wm.m_rating DESC """)
    result = cur.fetchone()
    average = MovieDetails.get_average(result[0])
    result_dict = {
        "m_id": result[0],
        "m_title": result[1],
        "m_poster": result[2],
        "m_imdb_rate": result[3],
        "m_year": result[4],
        "m_web_rate": average
    }
    comedy_list.append(result_dict)

    # Jojo Rabbit
    cur.execute(""" SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                            From web_movie wm
                            where UPPER(wm.m_title) = UPPER("Jojo Rabbit")
                            ORDER BY wm.m_rating DESC """)
    result = cur.fetchone()
    average = MovieDetails.get_average(result[0])
    result_dict = {
        "m_id": result[0],
        "m_title": result[1],
        "m_poster": result[2],
        "m_imdb_rate": result[3],
        "m_year": result[4],
        "m_web_rate": average
    }
    comedy_list.append(result_dict)

    # other comedy
    cur.execute(""" SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating, a.m_year
                        FROM web_movie a, movie_genre b, web_genre c
                        WHERE a.m_id = b.m_id
                        AND b.g_id = c.g_id
                        AND UPPER(c.g_name) like UPPER("%{}%") 
                        AND UPPER(c.g_name) not like UPPER("%{}%")
                        ORDER BY a.m_rating DESC""".format("comedy", "Short"))

    for result in cur.fetchall():
        if len(comedy_list) >= 9:
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
        if MovieUtil.is_movie_in_list(result_dict, comedy_list) and result_dict['m_poster'] is not None:
            comedy_list.append(result_dict)
    con.close()
    return comedy_list


def sci_ci_movie():
    """ help function for generate the sci-fi movies that need to be placed on homepage"""
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    # Sci-fi
    scifi_list = []
    # Inception
    cur.execute(""" SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                            From web_movie wm
                            where UPPER(wm.m_title) = UPPER("Inception")
                            ORDER BY wm.m_rating DESC """)
    result = cur.fetchone()
    average = MovieDetails.get_average(result[0])
    result_dict = {
        "m_id": result[0],
        "m_title": result[1],
        "m_poster": result[2],
        "m_imdb_rate": result[3],
        "m_year": result[4],
        "m_web_rate": average
    }
    scifi_list.append(result_dict)

    # The matrix
    cur.execute(""" SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                            From web_movie wm
                            where UPPER(wm.m_title) = UPPER("The Matrix")
                            ORDER BY wm.m_rating DESC """)
    result = cur.fetchone()
    average = MovieDetails.get_average(result[0])
    result_dict = {
        "m_id": result[0],
        "m_title": result[1],
        "m_poster": result[2],
        "m_imdb_rate": result[3],
        "m_year": result[4],
        "m_web_rate": average
    }
    scifi_list.append(result_dict)

    # The Terminator
    cur.execute(""" SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                    From web_movie wm
                    where UPPER(wm.m_title) like UPPER("%{}%")
                    ORDER BY wm.m_rating DESC """.format("The Terminator"))
    for result in cur.fetchall():
        if len(scifi_list) >= 9:
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
        scifi_list.append(result_dict)

    # other scifi
    cur.execute(""" SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating, a.m_year
                        FROM web_movie a, movie_genre b, web_genre c
                        WHERE a.m_id = b.m_id
                        AND b.g_id = c.g_id
                        AND UPPER(c.g_name) like UPPER("%{}%") 
                        AND UPPER(c.g_name) not like UPPER("%{}%")
                        ORDER BY a.m_rating DESC""".format("Sci-Fi", "Short"))

    for result in cur.fetchall():
        if len(scifi_list) >= 9:
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
        if MovieUtil.is_movie_in_list(result_dict, scifi_list) and result_dict['m_poster'] is not None:
            scifi_list.append(result_dict)
    con.close()
    return scifi_list


def crime_movie():
    """ help function for generate the crime movies that need to be placed on homepage"""
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    # Crime
    crime_list = []
    # The Godfather
    cur.execute(""" SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                        From web_movie wm
                        where UPPER(wm.m_title) like UPPER("%{}%")
                        ORDER BY wm.m_rating DESC """.format("The Godfather"))
    for result in cur.fetchall():
        if len(crime_list) >= 9:
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

        crime_list.append(result_dict)

    # 12 Angry Men
    cur.execute(""" SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                        From web_movie wm
                        where UPPER(wm.m_title) = UPPER("12 Angry Men")
                        ORDER BY wm.m_rating DESC """)
    for result in cur.fetchall():
        if len(crime_list) >= 9:
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

        crime_list.append(result_dict)

    # Pulp Fiction
    cur.execute(""" SELECT distinct wm.m_id, wm.m_title, wm.m_poster, wm.m_rating, wm.m_year
                        From web_movie wm
                        where UPPER(wm.m_title) = UPPER("Pulp Fiction")
                        ORDER BY wm.m_rating DESC """)
    for result in cur.fetchall():
        if len(crime_list) >= 9:
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

        crime_list.append(result_dict)

    # other crime
    cur.execute(""" SELECT distinct (a.m_id), a.m_title, a.m_poster, a.m_rating, a.m_year
                        FROM web_movie a, movie_genre b, web_genre c
                        WHERE a.m_id = b.m_id
                        AND b.g_id = c.g_id
                        AND UPPER(c.g_name) like UPPER("%{}%")
                        AND UPPER(c.g_name) not like UPPER("%{}%")
                        ORDER BY a.m_rating DESC""".format("Crime", "Short"))

    for result in cur.fetchall():
        if len(crime_list) >= 9:
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
        if MovieUtil.is_movie_in_list(result_dict, crime_list) and result_dict['m_poster'] is not None:
            crime_list.append(result_dict)
    con.close()
    return crime_list

