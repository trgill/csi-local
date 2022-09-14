#!/bin/bash -x
#
# Note: docker builds in /tmp/docker-xxx, so using relative paths
# to reference parent directories to build the image fails.

if [[ -z "$GITHUB_PAT" ]]; then
    echo "Must provide GITHUB_PAT with write access to ghcr.io/trgill/springfield-csi-driver in environment" 1>&2
    exit 1
fi

podman logout ghcr.io -u trgill

export VERSION="0.0.1"
podman build -f deploy/docker/Dockerfile --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') -t springfield-csi-driver:0.0.1 .

podman image ls localhost/springfield-csi-driver

echo $GITHUB_PAT | podman login ghcr.io -u trgill --password-stdin

podman tag springfield-csi-driver:$VERSION ghcr.io/trgill/springfield-csi-driver:$VERSION

podman push ghcr.io/trgill/springfield-csi-driver:$VERSION

podman images ghrc.io/trgill/
