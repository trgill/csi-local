#!/bin/bash -x

docker run -ti --rm \
     -v /var/run/dbus/system_bus_socket:/var/run/dbus/system_bus_socket \
      --privileged --user $(id -u):$(id -g) springfield-docker:devel --devices /dev/sda /dev/sdb

