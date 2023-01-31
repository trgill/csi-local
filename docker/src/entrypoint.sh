#!/bin/bash -x

echo "Starting container with: $@"

pwd

set +e
/usr/bin/python3 /docker-springfield-driver/main.py "$@"
set -e

echo "exiting script"
