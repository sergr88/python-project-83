from urllib import parse as urllib_parse

import requests
import validators
from bs4 import BeautifulSoup

from page_analyzer import db

_MAX_NAME_LENGTH = 255


def make(**kwargs):
    return kwargs


def validate(url):
    return validators.url(url['name']) and len(url['name']) <= _MAX_NAME_LENGTH


def normalize(url):
    parse_result = urllib_parse.urlparse(url['name'])
    return {'name': f'{parse_result.scheme}://{parse_result.hostname}'}


def save(url):
    query = """
        INSERT INTO urls (name) VALUES (%(name)s)
        ON CONFLICT DO NOTHING RETURNING id;
    """
    url_id = db.insert_if_not_exists(query, parameters=url)
    if url_id:
        url['id'] = url_id
        return True

    query = 'SELECT id FROM urls WHERE name = %(name)s;'
    urls = db.query(query, parameters={'name': url['name']})
    url['id'] = urls[0].id
    return False


def check(url):
    url = get_one_by_id(url['id'])

    response = requests.get(url.name, timeout=4, verify=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.select_one('html > body h1')
    title = soup.select_one('html > head > title')
    description = soup.select_one('html > head > meta[name="description"]')

    data = {
        'url_id': url.id,
        'status_code': response.status_code,
        'h1': h1.text if h1 else None,
        'title': title.text if title else None,
        'description': description.get('content') if description else None,
    }
    query = """
        INSERT INTO url_checks (url_id, status_code, h1, title, description)
        VALUES (%(url_id)s, %(status_code)s, %(h1)s, %(title)s,
                %(description)s);
    """
    db.insert(query, data)


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
    query = 'SELECT id, name, created_at::date FROM urls WHERE id = %(id)s;'
    urls = db.query(query, parameters={'id': id})
    return urls[0] if urls else None
