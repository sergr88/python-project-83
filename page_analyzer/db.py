import os

import dotenv
import psycopg2
from psycopg2.extras import NamedTupleCursor

dotenv.load_dotenv()
_DATABASE_URL = os.environ['DATABASE_URL']


def query(query, parameters=None):
    with (
        psycopg2.connect(_DATABASE_URL) as connection,
        connection.cursor(cursor_factory=NamedTupleCursor) as cursor,
    ):
        cursor.execute(query, parameters)
        return cursor.fetchall()


def insert(query, parameters=None):
    with (
        psycopg2.connect(_DATABASE_URL) as connection,
        connection.cursor(cursor_factory=NamedTupleCursor) as cursor,
    ):
        cursor.execute(query, parameters)


def insert_if_not_exists(query, parameters):
    with (
        psycopg2.connect(_DATABASE_URL) as connection,
        connection.cursor(cursor_factory=NamedTupleCursor) as cursor,
    ):
        cursor.execute(query, parameters)
        primary_key = cursor.fetchone()
        return primary_key[0] if primary_key else None
