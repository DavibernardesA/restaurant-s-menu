import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()

db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')

def connect_to_database():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host="db",
            port=5432
        )

        cur = conn.cursor()
#         cur.execute('''
# alter table menu
# add column description text,
# add column price decimal(10, 2),
# add column available boolean default true;
#     ''')
        cur.fetchall()
        conn.commit()
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
    return conn
