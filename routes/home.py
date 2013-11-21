from flask.ext.login import current_user
from flask import render_template, flash
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

from app import app
from models import Article, User, Share
from bi.parse_article import parse_article


class SendLinkForm(Form):
    url = TextField('url', validators=[DataRequired()])
    friend = TextField('friend', validators=[DataRequired()])


@app.route('/', methods=['POST', 'GET'])
def home():
    """Render website's home page."""
    if not current_user.is_authenticated():
        return render_template('splash.html')

    form = SendLinkForm()

    if form.validate_on_submit():
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

        flash("Successfully shared to %s" % user.get_name(), 'success')
        parse_article(article, share)

    received = current_user.receiving_shares.filter(Share.parsed == True) \
            .filter(Share.read_date == None) \
            .order_by(Share.created_date.desc()) \
            .limit(10).all()

    return render_template('home.html', user=current_user, form=form, shares=received)
