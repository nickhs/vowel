from flask import abort

from app import app
from models import Article


@app.route('/article/<int:article_id>', methods=['GET'])
def article(article_id):
    article = Article.query.get(article_id)
    if not article:
        return abort(404)

    return abort(200)
