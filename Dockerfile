FROM microservice
MAINTAINER Cerebro <cerebro@ganymede.eu>

RUN apt-get install -y python-yaml

ADD . /opt/example-multi
ADD ./supervisor/*.conf /etc/supervisor/conf.d/

EXPOSE 80
EXPOSE 81
