import psycopg2
from psycopg2.extras import NamedTupleCursor
import os
from dotenv import load_dotenv
import datetime


load_dotenv()


def init_connection():
    DATABASE_URL = os.getenv('DATABASE_URL')
    try:
        connection = psycopg2.connect(DATABASE_URL)
        return connection
    except Exception:
        print('Cant establish connection to database')


def get_cursor(connection):
    return connection.cursor(cursor_factory=NamedTupleCursor)


class DbManager:
    def insert_url(self, url):
        with init_connection() as conn:
            with get_cursor(conn) as cursor:
                date = datetime.date.today()
                cursor.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)",
                               (url, date))
                cursor.execute("SELECT * FROM urls WHERE name=%s", (url,))
                url = cursor.fetchone()
                return url

    def insert_url_check(self, url_id, response):
        with init_connection() as conn:
            with get_cursor(conn) as cursor:
                date = datetime.date.today()
                cursor.execute("INSERT INTO urls_checks (url_id, created_at, response_code) VALUES (%s, %s, %s)",
                               (url_id, date, response))

    def get_urls_list(self):
        with init_connection() as conn:
            with get_cursor(conn) as cursor:
                cursor.execute("SELECT * FROM urls ORDER BY id DESC;")
                all_users = cursor.fetchall()
                return all_users

    def is_url_in_bd(self, url):
        with init_connection() as conn:
            with get_cursor(conn) as cursor:
                cursor.execute("SELECT * FROM urls WHERE name=%s", (url,))
                desired_url = cursor.fetchone()
                if desired_url:
                    return True
                return False

    def is_url_id_in_bd(self, url_id):
        with init_connection() as conn:
            with get_cursor(conn) as cursor:
                cursor.execute('SELECT * FROM urls WHERE id=%s', (url_id,))
                desired_url = cursor.fetchone()
                if desired_url:
                    return True
                return False

    def get_url_from_urls_list(self, url_id):
        with init_connection() as conn:
            with get_cursor(conn) as cursor:
                cursor.execute("SELECT * FROM urls WHERE id=%s", (url_id,))
                desired_url = cursor.fetchone()
                if not desired_url:
                    return False
                return desired_url

    def get_url_from_urls_checks_list(self, url_id):
        with init_connection() as conn:
            with get_cursor(conn) as cursor:
                cursor.execute("SELECT * FROM urls_checks "
                               "WHERE url_id=%s ORDER BY created_at DESC, id DESC",
                               (url_id,))
                checks_list = cursor.fetchall()
                return checks_list

    def get_id_from_url(self, url):
        with init_connection() as conn:
            with get_cursor(conn) as cursor:
                cursor.execute("SELECT * FROM  urls WHERE name=%s", (url,))
                url_id = cursor.fetchone()
                if not url_id:
                    raise ValueError('Database doesnt contain this url!')
                return url_id.id

