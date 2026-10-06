import psycopg
import json

def connect_db():
    conn = psycopg.connect(
        dbname="lol_project",
        user="won",
        host="localhost"
    )
    print("Connected to PostgreSQL!")
    return conn

def insert_match(conn, match):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO raw_matches (match_id, raw_data)
            VALUES (%s, %s)
            ON CONFLICT (match_id) DO NOTHING
            """,
            (
                match["match_id"],
                json.dumps(match)
            )
        )
    conn.commit()