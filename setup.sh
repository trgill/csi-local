#!/bin/bash -x

export KUBERNETES_VERSION=v1.24.2
export HELM_VERSION=v3.10.3
export KIND_VERSION=v0.18.0

export BINDIR=./bin

export KIND=bin/kind
export KUBECTL=bin/kubectl
export HELM=bin/helm

export CSI_CONTAINER=springfield-csi-driver:devel

export CURL="curl -sSLf"

export CONTAINER_CMD=docker
export STRATIS_CMD=stratis

[[ $(type -P "$CONTAINER_CMD") ]] && echo "$CONTAINER_CMD is in PATH"  ||
    { echo "$CONTAINER_CMD is NOT in PATH, install $CONTAINER_CMD to continue" 1>&2; exit 1; }

[[ $(type -P "$STRATIS_CMD") ]] && echo "$STRATIS_CMD is in PATH"  ||
    { echo "$STRATIS_CMD is NOT in PATH, install $STRATIS_CMD to continue" 1>&2; exit 1; }

if [ ! -d "$BINDIR" ]; then
    mkdir -p bin
fi

# Install kind
if [ ! -f "$KIND" ]; then
    $CURL -Lo $KIND https://kind.sigs.k8s.io/dl/$KIND_VERSION/kind-linux-amd64
    chmod +x $KIND
fi

# Install kubectl
if [ ! -f "$KUBECTL" ]; then
    $CURL -Lo $KUBECTL  https://storage.googleapis.com/kubernetes-release/release/$KUBERNETES_VERSION/bin/linux/amd64/kubectl
    chmod 755 $KUBECTL
fi

# Install helm
if [ ! -f "$HELM" ]; then
    $CURL https://get.helm.sh/helm-$HELM_VERSION-linux-amd64.tar.gz \
            | tar xvz -C ./bin --strip-components 1 linux-amd64/helm
fi

if [ ! -f "$CSI_CONTAINER" ]; then
    $CONTAINER_CMD pull $CSI_CONTAINER
    $CONTAINER_CMD save -o $BINDIR/$CSI_CONTAINER:devel.image $CSI_CONTAINER
fi

