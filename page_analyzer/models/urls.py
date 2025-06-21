from urllib import parse as urllib_parse

import requests
import validators

from page_analyzer import db


def make(**kwargs):
    return kwargs


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
    urls = db.query(query, parameters={'name': url['name']})
    url['id'] = urls[0].id
    return False


def check(url):
    url = get_one_by_id(url['id'])
    response = requests.get(url['name'], timeout=10, verify=False)
    response.raise_for_status()
    data = {'url_id': url['id'], 'status_code': response.status_code}
    db.insert(table_name='url_checks', data=data)


def get_all():
    query = """
        SELECT DISTINCT ON (u.created_at)
               u.id,
               u.name,
               c.created_at::date AS checked_at,
               c.status_code
        FROM urls AS u
             LEFT JOIN url_checks AS c ON u.id = c.url_id
        ORDER BY u.created_at DESC, c.created_at DESC;
    """
    return db.query(query)


def get_one_by_id(id):
    query = 'SELECT id, name, created_at::date FROM urls WHERE id = :id;'
    urls = db.query(query, parameters={'id': id})
    return urls[0] if urls else None
