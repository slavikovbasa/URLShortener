FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DATABASE_URL=postgres://urlshort:qwerty123@localhost:5432/urlshort
ENV SECRET_KEY=gF1tGr6Rh75P+u4rEouCisLm4/3iQUGSDQYuWEfcwRw=
ENV FLASK_APP=urlshortener/app.py

CMD ["flask", "run"]