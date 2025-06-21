import os

import dotenv
import sqlalchemy
from sqlalchemy.dialects import postgresql

dotenv.load_dotenv()

_ENGINE = sqlalchemy.create_engine(os.environ['DATABASE_URL'])


def query(query, parameters=None):
    with _ENGINE.begin() as connection:
        cursor_result = connection.execute(sqlalchemy.text(query), parameters)
    return cursor_result.mappings().fetchall()


def insert(table_name, data):
    metadata = sqlalchemy.MetaData()
    table = sqlalchemy.Table(table_name, metadata, autoload_with=_ENGINE)
    with _ENGINE.begin() as connection:
        connection.execute(sqlalchemy.insert(table), data)


def insert_if_not_exists(table_name, data, constraint):
    metadata = sqlalchemy.MetaData()
    table = sqlalchemy.Table(table_name, metadata, autoload_with=_ENGINE)
    with _ENGINE.begin() as connection:
        statement = (postgresql.insert(table)
                     .values(data)
                     .on_conflict_do_nothing(constraint=constraint))
        primary_key = connection.execute(statement).inserted_primary_key
        return primary_key.id if primary_key else None
