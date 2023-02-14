#!/bin/bash -x

echo "Starting container springfield csi local...."

set +e
/usr/local/bin/python3 /csi-springfield-driver/server.py
set -e

ls -l /var/run/dbus

echo "starting bash"
/usr/bin/bash