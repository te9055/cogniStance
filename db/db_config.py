import sqlite3


def get_db():

    conn = sqlite3.connect('/Users/tom/PycharmProjects/cognistance/db/chinesedata.db')
    cursor = conn.cursor()
    return conn, cursor