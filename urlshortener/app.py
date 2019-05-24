'''Main application module. Includes all the flask views'''


from .forms import LoginForm, RegistrationForm
from .shorturl import encode, mix_number
from flask_login import current_user, login_user, logout_user
from flask_migrate import upgrade
from flask import render_template, redirect, url_for, flash, jsonify, request
from urlshortener import app, db
from urlshortener.models import User, Link


@app.route('/')
def index():
    '''Displays index.html, containing URL input field'''

    return render_template('index.html')


@app.route('/link/shorten', methods=['POST'])
def shorten_url():
    '''Shorten URL submitted by fetch script
    
    Saves full and shortened URL in database and
    returns json object with shortened URL back to fetch script
    '''

    input_url = request.form['input_url']
    author_id = current_user.id if current_user.is_authenticated else None
    app.logger.info('User ' + str(author_id) + 
                        ': Shorten URL request: ' + input_url)

    link = Link(full=input_url, user_id=author_id)
    db.session.add(link)
    db.session.flush()

    short_url = encode(mix_number(link.id))
    link.short = short_url
    app.logger.info('Shortened URL: ' + short_url + ' for ' + input_url)

    db.session.add(link)
    db.session.commit()
    app.logger.info('Shortened URL: ' + short_url + ' submitted to DB')

    return jsonify({'short': short_url})


@app.route('/<short_url>')
def redirect_url(short_url):
    '''Redirect from the shortened URL to the corresponding full URL'''

    link = Link.query.filter_by(short=short_url).first()
    if not link:
        app.logger.info('Redirect from: ' + short_url + ': 404 Not found')
        return '404 Not Found', 404

    full_url = link.full
    link.count += 1
    db.session.add(link)
    db.session.commit()
    app.logger.info('Redirect from: ' + short_url + ': ' + full_url)

    return redirect(full_url)


@app.route('/user/dashboard')
def dashboard():
    '''Display dashboard if user is autheticated, else redirect to login'''

    if current_user.is_authenticated:
        return render_template('dashboard.html', user=current_user)

    return redirect(url_for('login'))


@app.route('/user/login', methods=['GET', 'POST'])
def login():
    '''User Log In routine'''

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            app.logger.info(repr(user) + ' login failed')
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        app.logger.info(repr(user) + ' login successful')
        return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)


@app.route('/user/logout')
def logout():
    '''User logout routine'''

    if current_user.is_authenticated:
        app.logger.info(repr(current_user) + ' logged out')
        logout_user()
    
    return redirect(url_for('index'))


@app.route('/user/register', methods=['GET','POST'])
def register():
    '''User registration routine'''
    
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        app.logger.info(repr(user) + ' registration successful')
        return redirect(url_for('dashboard'))

    return render_template('registration.html', form=form)
