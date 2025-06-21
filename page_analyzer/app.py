import os

import flask

from page_analyzer import models

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/urls')
def urls_index():
    urls = models.urls.get_all()
    return flask.render_template('urls/index.html', urls=urls)


@app.route('/urls/<id>')
def urls_show(id):
    url = models.urls.get_one_by_id(id)
    if not url:
        flask.abort(404)

    url_checks = models.url_checks.get_all_by_url_id(id)
    messages = flask.get_flashed_messages(with_categories=True)
    return flask.render_template(
        'urls/show.html',
        url=url,
        url_checks=url_checks,
        messages=messages,
    )


@app.post('/urls')
def urls_post():
    url = models.urls.make(name=flask.request.form.get('url'))
    if not models.urls.validate(url):
        messages = [('danger', 'Некорректный URL')]
        return flask.render_template('index.html', url=url['name'], messages=messages), 422

    normalized_url = models.urls.normalize(url)
    url_is_new = models.urls.save(normalized_url)
    if url_is_new:
        flask.flash('Страница успешно добавлена', 'success')
    else:
        flask.flash('Страница уже существует', 'info')
    return flask.redirect(flask.url_for('urls_show', id=normalized_url['id']))


@app.post('/urls/<id>/checks')
def urls_check(id):
    url = models.urls.make(id=id)
    try:
        models.urls.check(url)
    except Exception:
        flask.flash('Произошла ошибка при проверке', 'danger')
    return flask.redirect(flask.url_for('urls_show', id=id))


@app.errorhandler(404)
def handle_404(error):
    return flask.render_template('404.html')
