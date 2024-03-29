FROM python:3.8

WORKDIR /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
EXPOSE 8000
CMD gunicorn music_events.wsgi:application --bind 0.0.0.0:8000
