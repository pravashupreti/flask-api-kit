FROM python:3.7

RUN apt update

RUN pip install pipenv
RUN pip install uwsgi

WORKDIR /app

COPY Pipfile* ./

RUN apt-get -y update
RUN apt-get -y install supervisor
RUN pipenv install --deploy --system
RUN apt-get install -y nginx

COPY . /app
COPY ./conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./conf/uwsgi.ini /etc/uwsgi/
COPY ./conf/flaskapikit.com /etc/nginx/sites-enabled/flaskapikit.com


ENV PORT=5000
EXPOSE 5000

CMD bash -c "if [ -n ${SEED_DATABASE} ]; then python seed_mock_data.py ; fi; alembic upgrade head ; exec /usr/bin/supervisord"
