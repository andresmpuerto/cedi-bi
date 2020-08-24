FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/venv
RUN mkdir -p /opt/app/backend
COPY requirements.txt start-server.sh /opt/app/
COPY .venv /opt/app/venv/
COPY . /opt/app/backend/
WORKDIR /opt/app
RUN pip install -r requirements.txt
# RUN chown -R www-data:www-data /opt/app

EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]