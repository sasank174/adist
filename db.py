import psycopg2

conn = None

def db_connect():
    global conn
    conn = psycopg2.connect(
        host = "ec2-54-157-16-125.compute-1.amazonaws.com",
        user = "znwahnrdcbtjjb",
        password = "a3b7b147ad6cbc9a3b07b51f02b9c96ca4d510607202f242706f54b255d58b2a",
        database = "d9mvoqrjshij7o"
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
    # cur.commit()
    cur.close()
    return True