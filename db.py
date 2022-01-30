import psycopg2

conn = None

def db_connect():
    global conn
    conn = psycopg2.connect(
        host = "ec2-54-208-139-247.compute-1.amazonaws.com",
        user = "tybhmztluykmru",
        password = "5c29670d25e170a51daa4c166c0bc96b7ceb17394141c9a3f2a5b733af64a2af",
        database = "d5jnruoa8i21tc"
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