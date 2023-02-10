#!/bin/bash -x

#
# Note: docker builds in /tmp/docker-xxx, so using relative paths
# to reference parent directories to build the image fails.

export CLUSTER_NAME=springfield-test
export KIND=bin/kind

$KIND delete cluster --name=$CLUSTER_NAME

$KIND create cluster --name=$CLUSTER_NAME --config tests/kind/springfield-cluster.yaml  

