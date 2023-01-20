#!/bin/bash -x

echo "Starting container csi....5"
which python3
ls
pwd

echo "show pip3 show  grpcio grpcio-tools protobuf dbus-python"
pip3 show  grpcio grpcio-tools protobuf dbus-python

/csi-springfield-driver/bin/livenessprobe &

set +e
/usr/bin/python3 /csi-springfield-driver/server.py
set -e

echo "exiting script"