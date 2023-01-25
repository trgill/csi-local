#!/bin/bash -x

docker run -ti --rm \
     -v /var/run/dbus/system_bus_socket:/var/run/dbus/system_bus_socket \
      --privileged \
     springfield-docker:devel



