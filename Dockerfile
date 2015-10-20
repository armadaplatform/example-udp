FROM microservice
MAINTAINER Cerebro <cerebro@ganymede.eu>

ADD . /opt/example-udp
ADD ./supervisor/* /etc/supervisor/conf.d/
RUN rm /etc/supervisor/conf.d/register_in_service_discovery.conf

EXPOSE 80
EXPOSE 200/udp
