from page_analyzer import db


def make(url_id):
    return {'url_id': url_id}


def save(url_check):
    db.insert(table_name='url_checks', data=url_check)


def get_by_url_id(url_id):
    query = """
        SELECT id, status_code, h1, title, description, created_at::date
        FROM url_checks
        WHERE url_id = :url_id
        ORDER BY url_checks.created_at DESC;
    """
    return db.execute_sql_query(query, parameters={'url_id': url_id})
