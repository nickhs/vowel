from flask.ext.login import current_user
from flask import render_template, flash, request, jsonify
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

from app import app
from models import Article, User, Share
from bi.parse_article import parse_article
from bi.utils import request_wants_json


class SendLinkForm(Form):
    url = TextField('url', validators=[DataRequired()])
    friend = TextField('friend', validators=[DataRequired()])


@app.route('/', methods=['POST', 'GET'])
def home():
    if request_wants_json(request):
        return _home_json()
    else:
        return _home_html()


def _home_json():
    if not current_user.is_authenticated():
        return jsonify({'success': False, 'reason': 'Not Authenticted'})

    form = SendLinkForm()
    if form.validate_on_submit():
        msg = _create_share(form)
        return jsonify({
            'success': True,
            'message': msg
        })

    # FIXME specify why validation failed

    return jsonify({
        'success': True,
        'shares': _get_received()
    })


def _home_html():
    """Render website's home page."""
    if not current_user.is_authenticated():
        return render_template('splash.html')

    form = SendLinkForm()

    if form.validate_on_submit():
        msg = _create_share(form)
        flash(msg, 'success')

    return render_template('home.html', user=current_user, form=form, shares=_get_received())


def _create_share(form):
    article = Article.query.filter_by(url=form.url.data).first()

    if not article:
        article = Article(form.url.data)
        article.save()

    user = User.query.filter_by(email=form.friend.data).first()
    if not user:
        user = User(form.friend.data)
        user.save()

    share = Share(current_user, user, article)
    share.save()

    parse_article(article, share)
    return "Successfully shared to %s" % user.get_name()


def _get_received(limit=10):
    received = current_user.receiving_shares.filter(Share.parsed == True) \
        .filter(Share.read_date == None) \
        .order_by(Share.created_date.desc()) \
        .limit(limit).all()

    return received
