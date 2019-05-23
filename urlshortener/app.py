from .forms import URLForm, LoginForm, RegistrationForm
from .shorturl import encode
from flask_login import current_user, login_user, logout_user
from flask import render_template, redirect, url_for, flash, jsonify, request
from urlshortener import app, login, db
from urlshortener.models import User, Link


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    return render_template('index.html', form=form)


@app.route('/link/shorten', methods=['POST'])
def shorten_url():
    input_url = request.form['input_url']
    author_id = current_user.id if current_user.is_authenticated else None
    link = Link(full=input_url, user_id=author_id)
    db.session.add(link)
    short_url = encode(link.id)
    link.short = short_url
    db.sessoin.add(link)
    db.session.commit()
    return jsonify({'short': short_url})


@app.route('/<short_url>')
def redirect_url(short_url):
    url = Link.query.filter_by(short=short_url).first()
    if not url:
        return '404 Not Found', 404
    
    return redirect(url.input_url)


@app.route('/user/dashboard', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html', user=current_user)

    return redirect(url_for(authenticate))


@app.route('/user/login', methods=['GET', 'POST'])
def authenticate(form):
    if current_user.is_authenticated:
        return redirect(url_for(dashboard))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        return signin(login_form)
    
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        return register(register_form)
    
    return render_template('authenticate.html',
        login_form=login_form, register_form=register_form
    )


@app.route('/user/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    
    return redirect(url_for(index))


def signin(form):
    user = User.query.filter_by(username=form.username.data).first()
    if not user or not user.check_password(form.password.data):
        flash('Invalid username or password')
        return redirect(url_for(authenticate))
    
    login_user(user, remember=form.remember_me.data)
    return redirect(url_for(dashboard))


def register(form):
    user = User(username=form.username)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=form.remember_me.data)
    return redirect(url_for(dashboard))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))