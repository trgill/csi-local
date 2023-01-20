#!/bin/bash -x

#
# Note: docker builds in /tmp/docker-xxx, so using relative paths
# to reference parent directories to build the image fails.

export CLUSTER_NAME=springfield-test
export KUBERNETES_VERSION=v1.24.2
export HELM_VERSION=v3.10.3
export BINDIR=./bin
export TMPDIR=/tmp/springfield
export CERT_MANAGER_VERSION=v1.7.0
export KIND_VERSION=v0.14.0
export KIND=bin/kind
export KUBECTL=bin/kubectl
export HELM=bin/helm
export CURL="curl -sSLf"
export LINVENESS_PROBE=bin/liveness

# CSI sidecar versions
export EXTERNAL_PROVISIONER_VERSION=3.2.1
export EXTERNAL_RESIZER_VERSION=1.5.0
export NODE_DRIVER_REGISTRAR_VERSION=2.5.1
export LIVENESSPROBE_VERSION=2.7.0
export EXTERNAL_SNAPSHOTTER_VERSION=6.0.1

export SIDECAR_SRC=sidecars
export LIVENESSPROBE_SRC=$SIDECAR_SRC/livenessprobe
export EXTERNAL_PROVISIONER_SRC=$SIDECAR_SRC/csi-provisioner
export NODE_DRIVER_REGISTRAR_SRC=$SIDECAR_SRC/node-driver-registrar
export EXTERNAL_RESIZER_SRC=$SIDECAR_SRC/external-resizer
export EXTERNAL_SNAPSHOTTER_SRC=$SIDECAR_SRC/external-snapshotter



mkdir -p "$SIDECAR_SRC"


if [[ -z "$GITHUB_PAT" ]]; then
    echo "Must provide GITHUB_PAT with write access to ghcr.io/trgill/springfield-csi-driver in environment" 1>&2
    exit 1
fi

if [ ! -d ./bin ]; then
    mkdir -p bin
fi

if [ ! -d $SIDECAR_SRC ]; then
    mkdir -p $SIDECAR_SRC
fi

# external-provisioner
if [ ! -d $EXTERNAL_PROVISIONER_SRC ]; then
    mkdir -p $EXTERNAL_PROVISIONER_SRC
fi

if [ ! -f ./bin/csi-provisioner ]; then
    $CURL https://github.com/kubernetes-csi/livenessprobe/archive/v$EXTERNAL_PROVISIONER_VERSION.tar.gz | tar zxf - --strip-components 1 -C $EXTERNAL_PROVISIONER_SRC
    make -C $EXTERNAL_PROVISIONER_SRC
    cp $EXTERNAL_PROVISIONER_SRC/bin/csi-provisioner ./bin
fi

# external-snapshotter
if [ ! -d $EXTERNAL_SNAPSHOTTER_SRC ]; then
    mkdir -p $EXTERNAL_SNAPSHOTTER_SRC
fi

if [ ! -f ./bin/csi-provisioner ]; then
    $CURL https://github.com/kubernetes-csi/livenessprobe/archive/v$EXTERNAL_SNAPSHOTTER_VERSION.tar.gz | tar zxf - --strip-components 1 -C $EXTERNAL_SNAPSHOTTER_SRC
    make -C $EXTERNAL_SNAPSHOTTER_SRC
    cp $EXTERNAL_SNAPSHOTTER_SRC/bin/csi-provisioner ./bin
fi

# external-resizer
if [ ! -d $EXTERNAL_RESIZER_SRC ]; then
    mkdir -p $EXTERNAL_RESIZER_SRC
fi

if [ ! -f ./bin/csi-provisioner ]; then
    $CURL https://github.com/kubernetes-csi/livenessprobe/archive/v$EXTERNAL_RESIZER_VERSION.tar.gz | tar zxf - --strip-components 1 -C $EXTERNAL_RESIZER_SRC
    make -C $EXTERNAL_RESIZER_SRC
    cp $EXTERNAL_RESIZER_SRC/bin/csi-provisioner ./bin
fi

# node-driver-registrar
if [ ! -d $NODE_DRIVER_REGISTRAR_SRC ]; then
    mkdir -p $NODE_DRIVER_REGISTRAR_SRC
fi

if [ ! -f ./bin/csi-provisioner ]; then
    $CURL https://github.com/kubernetes-csi/livenessprobe/archive/v$NODE_DRIVER_REGISTRAR_VERSION.tar.gz | tar zxf - --strip-components 1 -C $NODE_DRIVER_REGISTRAR_SRC
    make -C $NODE_DRIVER_REGISTRAR_SRC
    cp $NODE_DRIVER_REGISTRAR_SRC/bin/csi-provisioner ./bin
fi

# livenessprobe
if [ ! -d $LIVENESSPROBE_SRC ]; then
    mkdir -p $LIVENESSPROBE_SRC
fi

if [ ! -f ./bin/livenessprobe ]; then
    $CURL https://github.com/kubernetes-csi/livenessprobe/archive/v$LIVENESSPROBE_VERSION.tar.gz | tar zxf - --strip-components 1 -C $LIVENESSPROBE_SRC
    make -C $LIVENESSPROBE_SRC
    cp $LIVENESSPROBE_SRC/bin/livenessprobe ./bin
fi

exit 1

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


$KIND delete cluster --name=$CLUSTER_NAME


docker logout ghcr.io

export VERSION="0.1.0"

# TODO: Add logic to only build the container when necessary.
sudo docker build --no-cache -f deploy/docker/Dockerfile --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') -t springfield-csi-driver:devel .

# docker image ls localhost/springfield-csi-driver
echo $GITHUB_PAT | docker login ghcr.io -u trgill --password-stdin

sudo docker tag springfield-csi-driver:devel ghcr.io/trgill/springfield-csi-driver:devel
docker push ghcr.io/trgill/springfield-csi-driver:devel
docker save -o $BINDIR/springfield-csi-driver:devel.image ghcr.io/trgill/springfield-csi-driver:devel

docker images ghcr.io/trgill/springfield-csi-driver


# setup directories for building the kind cluster
rm -rf $TMPDIR || true
mkdir -p $TMPDIR || true
mkdir -p $TMPDIR/scheduler || true
mkdir -p $TMPDIR/controller || true
mkdir -p $TMPDIR/worker || true

mkdir -p $BINDIR || true

# copy kind config files
cp tests/kind/springfield-cluster.yaml $TMPDIR
cp deploy/scheduler/scheduler-config-v1beta2.yaml $TMPDIR/scheduler/scheduler-config.yaml

# create the cluster
$KIND create cluster --name=$CLUSTER_NAME --config $TMPDIR/springfield-cluster.yaml --image kindest/node:$KUBERNETES_VERSION

exit 0

# load the CSI driver to the new cluster
$KIND load image-archive --name=$CLUSTER_NAME $BINDIR/springfield-csi-driver:devel.image

$KUBECTL apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.7.0/cert-manager.crds.yaml
$KUBECTL create namespace springfield-system
$KUBECTL label namespace springfield-system springfield.redhat.com/webhook=ignore
$KUBECTL label namespace kube-system springfield.redhat.com/webhook=ignore

$HELM install --debug --namespace=springfield-system springfield ./deploy/helm/springfield-csi/ -f ./deploy/helm/springfield-csi/values.yaml


#$KUBECTL wait --for=condition=available --timeout=120s -n springfield-system deployments/springfield-controller
#$KUBECTL wait --for=condition=ready --timeout=120s -n springfield-system certificate/springfield-mutatingwebhook
#timeout 120 sh -c "until $KUBECTL apply -f ./tests/testpvc.yaml; do sleep 10; done"
#$KUBECTL wait --for=condition=ready --timeout=60s -n default pod -l app=example


if [[ -z "$GITHUB_PAT" ]]; then
    echo "Must provide GITHUB_PAT with write access to ghcr.io/trgill/springfield-csi-driver in environment" 1>&2
    exit 1
fi

