import forms
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = forms.URLForm()
    if form.validate_on_submit():
        url = form.url.data
        shortened = shorten(url)
        author = None
        if current_user.is_authenticated:
            author = current_user
        return shortened
    return render_template('index.html', form=form)

@app.route('/user/dashboard', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html', user=current_user)
    else:
        form = forms.LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            return username + password
        return render_template('login.html', form=form)

@app.route('/<short_url>')
def redirect_url(short_url):
    return short_url

def shorten(url):
    return 'yoshortyo'

if __name__ == "__main__":
    app.run(host="0.0.0.0")