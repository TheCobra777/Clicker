import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('clicker.db')
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        sql = ''' CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    clicks INTEGER DEFAULT 0
                  ); '''
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def get_user_clicks(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT clicks FROM users WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else 0

def update_user_clicks(conn, user_id, username, clicks):
    sql = ''' INSERT OR REPLACE INTO users(user_id, username, clicks)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (user_id, username, clicks))
    conn.commit()

conn = create_connection()
if conn is not None:
    create_table(conn)
else:
    print("Error! Cannot create the database connection.")
