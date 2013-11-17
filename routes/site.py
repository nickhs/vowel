from app import app

from flask import render_template
from flask.ext.security import login_required


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('splash.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.route('/test')
@login_required
def test():
    return render_template('home.html')
