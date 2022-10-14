""" Implementation for user_level.py """

import sqlite3
import movie.movie_util as MovieUtil


def level_up(u_id):
    """
    A function that level up the user's level
    The user's level will be capped on level 500
    The user will become a critic reviewer when they reach level 50

    Args:
        u_id: A string of user id

    Raises:
        Since this function will only be called from alter_exp(),
        so any exception will be handled in that function
    """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT u_level, u_is_critic_reviewer from web_user where u_id = ?", (u_id,))
    result = cur.fetchone()
    u_level = result[0] + 1
    if u_level <= 500:
        cur.execute(("UPDATE web_user SET u_level = ? where u_id = ?"), (u_level, u_id))

    if u_level >= 50 and result[1] == 0:
        cur.execute("UPDATE web_user SET u_is_critic_reviewer = 1 where u_id = '{}'".format(u_id))
    con.commit()
    con.close()


def alter_exp(u_id, exp):
    """
    A function that increase/decrease the user's experience
    When user's experience is larger than 2500 then the user will level up
    User's experience will not be grow after they reach level 500 and 2500 exp

    Args:
        u_id: A string of user id
        exp: A int that specified how much exp will the user gain or decrease

    Raises:
        Since this function will only be called from check_increase_or_decrease_exp(),
        revoke_exp() and post_review(), so any exception will be handled in that function
    """
    con = sqlite3.connect('data/db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT u_level, u_exp from web_user where u_id = ?", (u_id,))
    result = cur.fetchone()
    if result[0] < 500:
        u_exp = result[1] + exp
        if result[0] == 499 and u_exp >= 2500:
            u_exp = 2500
            level_up(u_id)
        elif result[0] != 499 and u_exp >= 2500:
            u_exp -= 2500
            level_up(u_id)
        cur.execute(("UPDATE web_user SET u_exp = ? where u_id = ?"), (u_exp, u_id))
        con.commit()
    con.close()


def check_increase_or_decrease_exp(u_id, ra_id):
    """
    A function that check if the user should gain/decrease experience
    depends on they receiving a like or dislike react for the review they post
    User gain 200 exp if they got a like react, other wise decrease by 20 exp

    Args:
        u_id: A string of user id
        ra_id: A string of react id

    Raises:
        Since this function will only be called from review_react(),
        so any exception will be handled in that function
    """
    ra_info = MovieUtil.get_ra_info(ra_id)
    if ra_info == "like":
        alter_exp(u_id, 200)
    elif ra_info == "dislike":
        alter_exp(u_id, -20)


def revoke_exp(u_id, ra_id):
    """
    A function that will revoke the exp they gain from the react
    if the react they got before is unreacted

    Args:
        u_id: A string of user id
        ra_id: A string of react id

    Raises:
        Since this function will only be called from review_react(),
        so any exception will be handled in that function
    """
    ra_info = MovieUtil.get_ra_info(ra_id)
    if ra_info == "like":
        alter_exp(u_id, -200)
    elif ra_info == "dislike":
        alter_exp(u_id, 20)
