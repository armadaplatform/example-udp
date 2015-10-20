# example-udp

`example-udp` demonstrates service that exposes UDP port, and shows various methods of accessing it by Armada's service discovery.

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

And `armada list` shows an additional subservice `example-udp:udp`:

    Name                 Address             ID            Status   Tags                
    example-udp          192.168.3.65:32777  4d4b25f4b2f2  passing  -                   
    example-udp:address  192.168.3.65:32788  4d4b25f4b2f2  passing  -            

The first port - 200/udp (`example-udp` on `armada list`) is the actual UDP server - simple echo server. 

The second port - 80/tcp (`example-udp:address` on `armada list`) is the address adapter to simplify getting access to UDP port. See below for more details.

The third port - 22/tcp is the SSH daemon.

You can play with the UDP server using nc/netcat: 
 
    $ nc -u 192.168.3.65 32777
    first line
    Reply from server: first line
    second line
    Reply from server:second line
    ^C

# Accessing the service.

The easiest way to access the UDP server from other Armada services would be to use `require_service` (See: http://armada.sh/docs/armada_features/service_discovery/),
If you wanted to use it from non-armada service, or from outside of the private network, the best solution would be magellan + main-haproxy duo.
Unfortunately, since this is UDP server, and not an HTTP server, you cannot use it.

However, you cas use the address adapter (running on HTTP) for acquiring the real UDP port.

Example with curl:

    curl 192.168.3.65:32788
    192.168.3.65:32777

Now you can configure your magellan to point `http://example-udp.initech.com` to `example-udp:address` and use it from anywhere. 

You can read more about setting up address adapter here: https://github.com/armadaplatform/example-multi
