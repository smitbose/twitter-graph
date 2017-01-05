import MySQLdb
import sys

conn = None

def open_connection():
    try:
        conn = MySQLdb.connect("localhost", "root", "1234", "twitter_graph")
    except:
        print(sys.exc_info())
        return

def get_connection():
    return conn

def close_connection():
    conn.close