FROM python:2.7.10

MAINTAINER Maslino liuxionghust@gmail.com

# update repo cache and install nginx
RUN apt-get update && apt-get install -y nginx

# create dirs
RUN mkdir -p /src/learning /data/log/uwsgi /data/log/nginx /data/log/supervisor /data/www/learning/media /data/www/learning/static

WORKDIR /src/learning

# copy source code
COPY . /src/learning

# copy nginx config file
COPY ./etc/default-site.conf /etc/nginx/sites-available/default

# copy supervisor config file
COPY ./etc/supervisord.conf /etc/supervisord.conf

# install dependencies
RUN pip install -r requirements.txt

# nginx listen on 80 port
EXPOSE 80

CMD /bin/sh /src/learning/run.sh
