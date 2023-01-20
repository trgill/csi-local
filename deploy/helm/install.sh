#!/bin/bash -x

# Note: Image is currently published as public.  Don't need to create secret.
# kubectl create secret docker-registry ghcr-login-secret --docker-server=https://ghcr.io --docker-username=$GITHUB_USER --docker-password=$GITHUB_USER --docker-email=$GITHUB_USER


# working around a problem with kind - this shouldn't be necessary
# follow: https://github.com/trgill/csi-local/issues/5 for details

# kind load docker-image ghcr.io/trgill/springfield-csi-driver:latest
CLUSTER_NAME := springfield-test

kind load image-archive --name=$(CLUSTER_NAME) build/topolvm.img;
