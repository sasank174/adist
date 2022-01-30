import psycopg2
from dotenv import load_dotenv
load_dotenv()
import os

conn = None

def db_connect():
    global conn
    conn = psycopg2.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )
    conn.autocommit = True
    return True

def select(query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows

def insert(query):
    cur = conn.cursor()
    cur.execute(query)
    cur.close()
    return True