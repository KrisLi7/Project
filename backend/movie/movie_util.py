"""
Implementation for movie_util.py
It contains all the helper functions for movie
"""

import sqlite3
from datetime import datetime


def generate_review_react_id():
    """ Generate a review react id """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT MAX(rr_id) FROM review_react")
    result = cur.fetchone()
    con.close()
    if result[0] is None:
        ms_id = 1
    else:
        ms_id = result[0] + 1
    return ms_id


def is_movie_exist(m_id):
    """ Check is the given m_id exist in database """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT m_id FROM web_movie where m_id = ?"), (m_id,))
    result = cur.fetchone()
    con.close()
    if result is not None:
        return True
    return False


def is_person_exist(p_id):
    """ Check is the given p_id exist in database """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT p_id FROM web_person where p_id = ?"), (p_id,))
    result = cur.fetchone()
    con.close()
    if result is not None:
        return True
    return False


def is_review_exist(r_id):
    """ Check is the given r_id exist in database """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT m_id FROM web_movie_review where r_id = ?"), (r_id,))
    result = cur.fetchone()
    con.close()
    if result is not None:
        return True
    return False


def is_react_exist(ra_id):
    """ Check is the given ra_id exist in database """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute(("SELECT ra_id FROM web_react where ra_id = ?"), (ra_id,))
    result = cur.fetchone()
    con.close()
    if result is not None:
        return True
    return False


def is_rate_valid(rate):
    """ Check is the rate is >=0 and <=5 """
    return bool((rate >= 0) & (rate <= 5))


def is_movie_in_list(result, list_dict):
    """ Check is the given movie dict exist in the given movie list """
    for cur_dict in list_dict:
        if cur_dict['m_id'] == result['m_id']:
            return False
    return True


def unix_datetime():
    """ Return current datetime as string """
    time = datetime.now()
    return time.strftime("%Y/%m/%d %H:%M:%S")


def insert_review_react(u_id, r_id, ra_id):
    """ Insert the given variable into the table review_react in database """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    rr_id = generate_review_react_id()

    query = "INSERT INTO review_react(rr_id, ra_id, r_id, u_id) VALUES (?, ?, ?, ?)"
    cur.execute(query, (rr_id, ra_id, r_id, u_id))
    con.commit()
    con.close()


def review_unreact(u_id, r_id):
    """ Unreact a review (delete the given variable from the table review_react) """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    query = "DELETE FROM review_react WHERE u_id = ? AND r_id = ?"
    cur.execute(query, (u_id, r_id))
    con.commit()
    con.close()


def count_like_react(r_id):
    """ Count how many user has like the corresponding review """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    query = """
            SELECT COUNT(rr.rr_id) FROM review_react rr
            JOIN web_react wr ON (rr.ra_id = wr.ra_id)
            WHERE rr.r_id = '{}' AND wr.ra_info = 'like'
            """.format(r_id)
    cur.execute(query)
    result = cur.fetchone()[0]
    con.close()
    return result


def count_dislike_react(r_id):
    """ Count how many user has dislike the corresponding review """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    query = """
            SELECT COUNT(rr.rr_id) FROM review_react rr
            JOIN web_react wr ON (rr.ra_id = wr.ra_id)
            WHERE rr.r_id = '{}' AND wr.ra_info = "dislike"
            """.format(r_id)
    cur.execute(query)
    result = cur.fetchone()[0]
    con.close()
    return result


def get_ra_info(ra_id):
    """ Get the react info by the given ra_id (like/dislike) """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    query = """
            SELECT ra_info FROM web_react
            WHERE ra_id = '{}'
            """.format(ra_id)
    cur.execute(query)
    ra_info = cur.fetchone()[0]
    con.close()
    return ra_info


def check_is_user_react_like(r_id, u_id):
    """ Check is the given user has like the given review """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("""
        SELECT COUNT(rr.rr_id) FROM review_react rr
        JOIN web_react wr ON (rr.ra_id = wr.ra_id)
        WHERE rr.r_id = '{}'
        And rr.u_id = '{}'
        AND wr.ra_info = "like"
    """.format(r_id, u_id))
    result = cur.fetchone()
    if result[0] > 0:
        return True
    return False


def check_is_user_react_dislike(r_id, u_id):
    """ Check is the given user has dislike the given review """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("""
        SELECT COUNT(rr.rr_id) FROM review_react rr
        JOIN web_react wr ON (rr.ra_id = wr.ra_id)
        WHERE rr.r_id = '{}'
        And rr.u_id = '{}'
        AND wr.ra_info = "dislike"
    """.format(r_id, u_id))
    result = cur.fetchone()
    if result[0] > 0:
        return True
    return False
