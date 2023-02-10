#!/bin/bash -x

echo "Starting container csi....6"
which python3
ls
ls /csi
pwd

which pip3

echo "show pip3 show  grpcio grpcio-tools protobuf dbus-python"
pip3 show  grpcio grpcio-tools protobuf dbus-python
pip3 install  grpcio grpcio-tools protobuf dbus-python

set +e
/usr/local/bin/python3 /csi-springfield-driver/server.py
set -e

ls -l /var/run/dbus

echo "starting bash"
/usr/bin/bash