FROM microservice
MAINTAINER Cerebro <cerebro@ganymede.eu>

ADD . /opt/example-udp
ADD ./supervisor/* /etc/supervisor/conf.d/

EXPOSE 80
EXPOSE 200/udp
