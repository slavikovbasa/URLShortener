FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DATABASE_URL=postgres://urlshort:qwerty123@postgres:5432/urlshort
ENV SECRET_KEY=gF1tGr6Rh75P+u4rEouCisLm4/3iQUGSDQYuWEfcwRw=

CMD ["python", "urlshortener/app.py"]