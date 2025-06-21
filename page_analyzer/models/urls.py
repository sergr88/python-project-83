from urllib import parse as urllib_parse

import validators

from page_analyzer import db


def make(name):
    return {'name': name}


def validate(url):
    return validators.url(url['name'])


def normalize(url):
    parse_result = urllib_parse.urlparse(url['name'])
    return {'name': f'{parse_result.scheme}://{parse_result.hostname}'}


def save(url):
    url_id = db.insert_if_not_exists(table_name='urls', data=url, constraint='urls_uq')
    if url_id:
        url['id'] = url_id
        return True

    query = 'SELECT id FROM urls WHERE name = :name;'
    urls = db.execute_sql_query(query, parameters={'name': url['name']})
    url['id'] = urls[0].id
    return False


def get_all():
    query = 'SELECT id, name, created_at::date FROM urls ORDER BY urls.created_at DESC;'
    return db.execute_sql_query(query)


def get_one(id):
    query = 'SELECT id, name, created_at::date FROM urls WHERE id = :id;'
    urls = db.execute_sql_query(query, parameters={'id': id})
    return urls[0] if urls else None
