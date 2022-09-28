#!/bin/bash

echo "Starting container...."
which python3
ls

set +e
exec /usr/bin/python3 /csi-springfield-driver/server.py $@
set -e

echo "python done... starting sleep"

sleep 1200

echo "exiting script"