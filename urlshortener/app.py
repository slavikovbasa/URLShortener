from urlshortener import app, login, db
from urlshortener.models import User, Url
from .forms import URLForm, LoginForm, RegistrationForm
from flask_login import current_user, login_user
from flask import render_template, redirect, url_for, flash


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url_data = form.url.data
        shortened = shorten(url_data)
        author_id = None
        if current_user.is_authenticated:
            author_id = current_user.id
        url = Url(shortened_url=shortened, input_url=url_data, user_id=author_id)
        return shortened
    return render_template('index.html', form=form)


@app.route('/user/dashboard', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html', user=current_user)

    signin_form = LoginForm()
    if signin_form.validate_on_submit():
        return login(signin_form)
    
    signup_form = RegistrationForm()
    if signup_form.validate_on_submit():
        return register(signup_form)

    return render_template('login.html', signin_form=signin_form, signup_form=signup_form)


def login(form):
    user = User.query.filter_by(username=form.username.data).first()
    if not user or not user.check_password(form.password.data):
        flash('Invalid username or password')
        return redirect(url_for(dashboard))
    login_user(user, remember=form.remember_me.data)
    return render_template('dashboard.html', user=current_user)


def register(form):
    user = User(username=form.username)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return render_template('dashboard.html', user=current_user)


@app.route('/<short_url>')
def redirect_url(short_url):
    url = Url.query.filter_by(shortened_url=short_url).first()
    if not url:
        return '404', 404
    
    return redirect(url.input_url)


def shorten(url):
    return 'yoshortyo'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))