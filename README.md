# example-udp

`example-udp` demonstrates service that exposes UDP port, and shows various methods of accessing it by Armada's service
discovery.

# Building and running the service.


    armada build example-udp
    armada run example-udp -d local


# Using the service.

After running the service we can see it exposes three ports:

    Running microservice example-udp from dockyard:  (alias: local) locally...
    Service is running in container 4d4b25f4b2f2 available at addresses:
      192.168.3.65:32777 (200/udp)
      192.168.3.65:32788 (80/tcp)
      192.168.3.65:32789 (22/tcp)

And `armada list` shows an additional subservice `example-udp:address`:

    Name                 Address             ID            Status   Tags                
    example-udp          192.168.3.65:32777  4d4b25f4b2f2  passing  -                   
    example-udp:address  192.168.3.65:32788  4d4b25f4b2f2  passing  -            

The first port - 200/udp (`example-udp` on `armada list`) is the actual UDP server - simple echo server. 

The second port - 80/tcp (`example-udp:address` on `armada list`) is the address adapter to simplify getting access to
UDP port. See below for more details.

The third port - 22/tcp is the SSH daemon.

You can play with the UDP server using nc/netcat: 
 
    $ nc -u 192.168.3.65 32777
    first line
    Reply from server: first line
    second line
    Reply from server:second line
    ^C

# Accessing the service.

The easiest way to access the non HTTP servers from other Armada services would be to use `require_service`
(See: http://armada.sh/docs/armada_features/service_discovery/), but we cannot use it here because HAProxy does not
support UDP.

However, you can use the address adapter (which is running on HTTP) for acquiring the actual UDP port.

Example with curl:

    $ curl 192.168.3.65:32788
    192.168.3.65:32777

As you can see it's the port of the UDP server.

Now you may use any Armada's service discovery mechanism for getting access to `example-udp:address`, and possibly
caching the response in your dependant service.

You can read more about setting up address adapter here: https://github.com/armadaplatform/example-multi

# Registering UDP service in Armada catalog.

There is a slight difference in registering UDP service from TCP.

Let's assume the UDP server is running on port 200, as this one is.
You have to expose this port in [Dockerfile](Dockerfile) using `EXPOSE 200/udp`.

And register it using similar [supervisor config](supervisor/udp_echo_server.conf):

    [program:register_udp_echo_server]
    directory=/opt/microservice/src
    command=python register_in_service_discovery.py 200/udp

Since Armada assumes the default service is running on 80/tcp, and tries to register it, we also have to turn it off
by removing supervisor config responsible for it.
It is enough to add this line to [Dockerfile](Dockerfile) to do that:

    RUN rm /etc/supervisor/conf.d/register_in_service_discovery.conf
