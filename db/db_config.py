import sqlite3


def get_db():

    conn = sqlite3.connect('/Users/tom/PycharmProjects/cognistance/db/datasets.db')
    cursor = conn.cursor()
    return conn, cursor