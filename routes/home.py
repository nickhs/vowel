from flask.ext.login import current_user
from flask import render_template
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

from app import app


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
        import pdb; pdb.set_trace()

    return render_template('home.html', user=current_user, form=form)
