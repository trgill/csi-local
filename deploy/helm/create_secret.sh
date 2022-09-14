#!/bin/bash -x

if [[ -z "$GITHUB_USER" ]]; then
    echo "Must provide GITHUB_USER in environment" 1>&2
    exit 1
fi

if [[ -z "$USER_EMAIL" ]]; then
    echo "Must provide USER_EMAIL in environment" 1>&2
    exit 1
fi

if [[ -z "$GITHUB_PAT" ]]; then
    echo "Must provide USER_EMAIL in environment" 1>&2
    exit 1
fi

kubectl create secret docker-registry springfield-csi-secret --docker-server=ghcr.io --docker-username=$GITHUB_USER --docker-password=$GITHUB_PAT --docker-email=$USER_EMAIL
