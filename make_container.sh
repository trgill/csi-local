#!/bin/bash -x


# TODO: Add logic to only build the container when necessary.
sudo docker build --no-cache -f deploy/docker/Dockerfile --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') -t springfield-docker:devel .

echo $GITHUB_PAT | docker login ghcr.io -u trgill --password-stdin

sudo docker tag springfield-docker:devel ghcr.io/trgill/springfield-docker:devel
docker push ghcr.io/trgill/springfield-docker:devel
docker save -o $BINDIR/springfield-docker:devel.image ghcr.io/trgill/springfield-docker:devel

docker images ghcr.io/trgill/springfield-docker



