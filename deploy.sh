#!/bin/bash -x

#
# Note: docker builds in /tmp/docker-xxx, so using relative paths
# to reference parent directories to build the image fails.



export CERT_MANAGER_VERSION=v1.7.0
export KIND_VERSION=v0.14.0
export KIND=bin/kind
export KUBECTL=bin/kubectl
export HELM=bin/helm
export BINDIR=./bin
export CLUSTER_NAME=springfield-test

export VERSION="0.1.1"

$KUBECTL apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.7.0/cert-manager.crds.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-provisioner/v1.5.0/deploy/kubernetes/rbac.yaml
$KUBECTL create namespace springfield-system
$KUBECTL label namespace springfield-system springfield.redhat.com/webhook=ignore
$KUBECTL label namespace kube-system springfield.redhat.com/webhook=ignore

$HELM install --debug --namespace=springfield-system springfield ./deploy/helm/springfield-csi/ -f ./deploy/helm/springfield-csi/values.yaml

#$KUBECTL wait --for=condition=available --timeout=120s -n springfield-system ./deploy/helm/springfield-csi 
#$KUBECTL wait --for=condition=ready --timeout=120s -n springfield-system certificate/springfield-mutatingwebhook

$KUBECTL get storageclass 

#timeout 120 sh -c "until $KUBECTL apply -f ./tests/testpvc.yaml; do sleep 10; done"
#$KUBECTL wait --for=condition=ready --timeout=60s -n default pod -l app=example
