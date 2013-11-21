from flask import render_template

from app import app, config, login_manager
from routes import __all__
from models import User

_pyflakes = __all__  # to pass pyflakes


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == '__main__':
    app.run(port=config.get('PORT', 8000),
            debug=config.get('DEBUG', False), host="0.0.0.0")
