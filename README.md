Simple URL Shortener
===========================

EVO Summer Python Lab '19 [Test task 1]

URL Shortener web server on Flask + PostgreSQL (basically any other DB supported by SQLAlchemy can be used).

URL shortening requests are handeled with fetch.
Login and signup forms use WTForms.

Starting Flask Web Server
============================

In order to start server, make sure that PostgreSQL instance is running and add corresponding DATABASE_URL environment variable.
Make sure that SECRET_KEY environment variable is also set.
Also FLASK_APP environment variable has to be set in order to be able to use flask command:

``export FLASK_APP=urlshortener/app.py``

Upgrade database (create all the tables):

``flask db upgrade``

Launch flask web server (use your values for host and port):

``flask run --host=0.0.0.0 --port=80``

Using docker
----------------------------

You can use docker to start server.
Make sure PostgreSQL instance in running.
Change DATABASE_URL and SECRET_KEY environment variables in Dockerfile to corresponding values (or submit corresponding values in ``docker run`` command)

Build image:

``docker build -t urlshortener .``

Run docker container:

``docker run --rm --net=host urlshortener bash -c "flask db upgrade && flask run --host=0.0.0.0 --port=80"``
