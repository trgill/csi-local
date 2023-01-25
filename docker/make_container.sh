#!/bin/bash -x


docker build --network host --no-cache -f Dockerfile --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') -t springfield-docker:devel .

