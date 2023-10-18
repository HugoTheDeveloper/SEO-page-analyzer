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
                cursor.execute("INSERT INTO urls (name, created_at) "
                               "VALUES (%s, %s)", (url, date))
                cursor.execute("SELECT * FROM urls WHERE name=%s", (url,))
                url = cursor.fetchone()
                return url

    def insert_url_check(self, url_id, response, h1, title, content):
        with init_connection() as conn:
            with get_cursor(conn) as cursor:
                date = datetime.date.today()
                cursor.execute("INSERT INTO urls_checks (url_id, created_at, "
                               "response_code, h1, title, description) "
                               "VALUES (%s, %s, %s, %s, %s, %s)",
                               (url_id, date, response, h1, title, content))

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
                               "WHERE url_id=%s ORDER BY id DESC",
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

    def get_urls_list(self):
        with init_connection() as conn:
            with get_cursor(conn) as cursor:
                cursor.execute("SELECT DISTINCT url_id, max(id) AS "
                               "id FROM urls_checks GROUP BY url_id")
                checks = cursor.fetchall()
                last_checks = tuple((check.id for check in checks))
                if not last_checks:
                    cursor.execute("SELECT name, id FROM urls;")
                    return cursor.fetchall()
                cursor.execute("CREATE TEMP TABLE last_checks "
                               "AS SELECT url_id, id, response_code, "
                               "created_at FROM urls_checks WHERE id in %s;",
                               (last_checks,))
                cursor.execute("SELECT urls.id AS id, urls.name AS name, "
                               "last_checks.response_code AS response_code, "
                               "last_checks.created_at AS created_at "
                               "FROM urls LEFT JOIN last_checks ON "
                               "urls.id = last_checks.url_id "
                               "ORDER BY id DESC")
                desired_urls = cursor.fetchall()
                return desired_urls
