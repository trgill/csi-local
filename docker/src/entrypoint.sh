#!/bin/bash -x

echo "Starting container"
which python3
ls
pwd

pip3 install dbus-python
pip3 show dbus-python

ping -c 3 192.168.122.105

set +e
/usr/bin/python3 /csi-springfield-driver/main.py
set -e

echo "exiting script"
