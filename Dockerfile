FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/static
COPY requirements.txt /opt/app/
COPY . /opt/app/
WORKDIR /opt/app
RUN pip install -r requirements.txt