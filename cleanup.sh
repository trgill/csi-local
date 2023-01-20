#!/bin/bash -x

export KIND=bin/kind
export CLUSTER_NAME=springfield-test

$KIND delete cluster --name=$CLUSTER_NAME

