#!/bin/bash -x

# Note: Image is currently published as public.  Don't need to create secret.
# kubectl create secret docker-registry ghcr-login-secret --docker-server=https://ghcr.io --docker-username=$GITHUB_USER --docker-password=$GITHUB_USER --docker-email=$GITHUB_USER

helm install --debug springfield-csi springfield-csi

helm get manifest springfield-csi
