#!/bin/bash -x

#
# Note: docker builds in /tmp/docker-xxx, so using relative paths
# to reference parent directories to build the image fails.



export KUBECTL=bin/kubectl
$KUBECTL apply -f ./tests/testpvc.yaml

