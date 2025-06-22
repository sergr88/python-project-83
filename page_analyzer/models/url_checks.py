from page_analyzer import db


def get_all_by_url_id(url_id):
    query = """
        SELECT id, status_code, h1, title, description, created_at::date
        FROM url_checks
        WHERE url_id = %(url_id)s
        ORDER BY url_checks.created_at DESC;
    """
    return db.query(query, parameters={'url_id': url_id})
