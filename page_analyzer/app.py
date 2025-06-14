import os
from urllib import parse as urllib_parse

import flask
import validators

from page_analyzer import lib

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/urls')
def urls_index():
    query = 'SELECT id, name, created_at::date FROM urls ORDER BY urls.created_at DESC;'
    urls = lib.execute_sql_query(query)
    return flask.render_template('urls/index.html', urls=urls)


@app.route('/urls/<id>')
def urls_show(id):
    query = 'SELECT id, name, created_at::date FROM urls WHERE id = :id;'
    urls = lib.execute_sql_query(query, parameters={'id': id})

    if not urls:
        flask.abort(404)

    messages = flask.get_flashed_messages(with_categories=True)
    return flask.render_template('urls/show.html', url=urls[0], messages=messages)


@app.post('/urls')
def urls_post():
    url = flask.request.form.get('url')
    if not validators.url(url):
        messages = [('danger', 'Некорректный URL')]
        return flask.render_template('index.html', url=url, messages=messages), 422

    parse_result = urllib_parse.urlparse(url)
    normalized_url = f'{parse_result.scheme}://{parse_result.hostname}'
    data = {'name': normalized_url}
    url_id = lib.insert_if_not_exists(table_name='urls', data=data, constraint='urls_uq')
    if url_id:
        flask.flash('Страница успешно добавлена', 'success')
    else:
        query = 'SELECT id FROM urls WHERE name = :name;'
        urls = lib.execute_sql_query(query, parameters={'name': normalized_url})
        url_id = urls[0].id
        flask.flash('Страница уже существует', 'info')
    return flask.redirect(flask.url_for('urls_show', id=url_id))


@app.errorhandler(404)
def handle_404(error):
    return flask.render_template('404.html')
