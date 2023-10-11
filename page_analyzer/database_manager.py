import psycopg2
from psycopg2.extras import NamedTupleCursor
import os
from dotenv import load_dotenv
import datetime
from urllib.parse import urlparse


load_dotenv()


def init_connection():
    DATABASE_URL = os.getenv('DATABASE_URL')
    try:
        connection = psycopg2.connect(DATABASE_URL)
        return connection
    except:
        print('Cant establish connection to database')


def get_cursor(connection):
    return connection.cursor(cursor_factory=NamedTupleCursor)


class DbManager:
    def insert_url(self, url):
        with init_connection() as conn:
            with get_cursor(conn) as cursor:
                date = datetime.date.today()
                url = urlparse(url)
                normalized_url = url.scheme + url.netloc
                cursor.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)",
                               (normalized_url, date))



