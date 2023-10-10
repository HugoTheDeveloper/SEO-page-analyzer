import psycopg2
from psycopg2.extras import NamedTupleCursor
import os
from dotenv import load_dotenv


load_dotenv()
print(os.getenv('DATABASE_URL'))


def init_connection():
    DATABASE_URL = os.getenv('DATABASE_URL')
    print(DATABASE_URL)
    try:
        connection = psycopg2.connect(DATABASE_URL)
        return connection
    except:
        print('Cant establish connection to database')

init_connection()

