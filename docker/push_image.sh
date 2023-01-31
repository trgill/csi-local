#!/bin/bash -x

echo $GITHUB_PAT | docker login ghcr.io -u trgill --password-stdin

sudo docker tag springfield-docker:devel ghcr.io/trgill/springfield-docker:devel
docker push ghcr.io/trgill/springfield-docker:devel
docker save -o $BINDIR/springfield-docker:devel.image ghcr.io/trgill/springfield-docker:devel

docker images ghcr.io/trgill/springfield-docker