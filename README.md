# example-multi

`example-multi` demonstrates ability to register multiple services in Armada catalog from single container.


# Address adapter.

The service also shows example usage of `address_adapter`. It's a helper component embedded in base `microservice` image
that can be used for connecting to non-HTTP services via DNS. Its only purpose is to serve service address
via HTTP protocol.

For example let's assume we have armadized `redis-master` service and don't want to run it binded to specific port.
We can run `address_adapter` inside the container and then access redis like this (error checks omitted for clarity):

    redis_address = requests.get("http://redis-master.initech.com")
    (redis_host, redis_port) = redis_address.split(':')
    redis_connection = redis.StrictRedis(host = redis_host, port = redis_port, ...)

To be able to access it that way we have to do 3 steps:


1. Add following lines to the [supervisor configuration](supervisor/address_adapter.conf):

        [program:address_adapter]
        directory=/opt/microservice/src
        command=python address_adapter.py 81

        [program:register_adapter]
        directory=/opt/microservice/src
        command=python register_in_service_discovery.py 81 -s address


2. Expose `address_adapter`'s port in [Dockerfile](Dockerfile):

        EXPOSE 81


3. configure `magellan` + `main-haproxy` to redirect domain `redis-master.initech.com` to subservice `redis-master:address`.


The above method is one of many ways that can be used for service discovery in Armada cluster.


# API (REST)

* `/` - Returns list of container's environment variables in json format.


# Building and running the service.

    armada build example-multi
    armada run example-multi

Using `armada list` we can see that the service registers 3 different endpoints in Armada catalog:

    Name                   Address             ID            Status   Tags
    example-multi          192.168.3.45:32800  5431ea66eb24  passing  -
    example-multi:address  192.168.3.45:32802  5431ea66eb24  passing  -
    example-multi:ssh      192.168.3.45:32798  5431ea66eb24  passing  -

We can also see that the `address_adapter` is working properly:

    admin@initech$ echo `curl -s 192.168.3.45:32802`
    192.168.3.45:32800
