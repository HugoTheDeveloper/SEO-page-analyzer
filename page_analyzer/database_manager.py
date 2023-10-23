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


def execute_in_bd(func):
    def inner(*args, **kwargs):
        with init_connection() as conn:
            with get_cursor(conn) as cursor:
                result = func(cursor=cursor, *args, **kwargs)
                return result
    return inner


class DbManager:
    @execute_in_bd
    def insert_url(self, url, cursor=None):
        date = datetime.date.today()
        cursor.execute("INSERT INTO urls (name, created_at) "
                       "VALUES (%s, %s)", (url, date))
        cursor.execute("SELECT * FROM urls WHERE name=%s", (url,))
        url = cursor.fetchone()
        return url

    @execute_in_bd
    def insert_url_check(self, check, cursor=None):
        date = datetime.date.today()
        cursor.execute("INSERT INTO urls_checks (url_id, created_at, "
                       "response_code, h1, title, description) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (check['url_id'], date, check['response'],
                        check["h1"], check['title'], check['content']))

    @execute_in_bd
    def is_url_in_bd(self, url, cursor=None):
        cursor.execute("SELECT * FROM urls WHERE name=%s", (url,))
        desired_url = cursor.fetchone()
        if desired_url:
            return True
        return False

    @execute_in_bd
    def get_url_from_urls_list(self, url_id, cursor=None):
        cursor.execute("SELECT * FROM urls WHERE id=%s", (url_id,))
        desired_url = cursor.fetchone()
        if not desired_url:
            return False
        return desired_url

    @execute_in_bd
    def get_url_from_urls_checks_list(self, url_id, cursor=None):
        cursor.execute("SELECT * FROM urls_checks "
                       "WHERE url_id=%s ORDER BY id DESC",
                       (url_id,))
        checks_list = cursor.fetchall()
        return checks_list

    @execute_in_bd
    def get_id_from_url(self, url, cursor=None):
        cursor.execute("SELECT * FROM  urls WHERE name=%s", (url,))
        url_id = cursor.fetchone()
        if not url_id:
            raise ValueError('Database doesnt contain this url!')
        return url_id.id

    @execute_in_bd
    def get_urls_list(self, cursor=None):
        cursor.execute("SELECT DISTINCT url_id, max(id) AS "
                       "id FROM urls_checks GROUP BY url_id")
        checks = cursor.fetchall()
        # print(checks)
        # cursor.execute('SELECT DISTINCT ON (url_id, max(id)) url_id, id, response_code, created_at'
        #                ' FROM urls_checks GROUP BY url_id, id, response_code')
        # print(cursor.fetchall())
        # cursor.execute('SELECT DISTINCT ON (url_id) url_id, max(id) AS id FROM urls_checks GROUP BY url_id '
        #                'RIGHT JOIN urls ON urls.id = urls_checks.url_id ORDER BY id DESC')
        # print(cursor.fetchall())
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
