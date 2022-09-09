
set -e
set -o pipefail

BASE_DIR="$( cd "$( dirname "$0" )" && pwd )"

TEMP_DIR="$( mktemp -d )"
#trap 'rm -rf ${TEMP_DIR}' EXIT


# Some images are not affected by *_REGISTRY/*_TAG and IMAGE_* variables.
# The default is to update unless explicitly excluded.
update_image () {
    case "$1" in socat) return 1;; esac
}

echo $TEMP_DIR

for component in csi-springfield-driverinfo.yaml csi-springfield-plugin.yaml csi-springfield-testing.yaml csi-springfield-snapshotclass.yaml; do
    
    cp springfield/"${component}" "${TEMP_DIR}"/rbac.yaml

    cat <<- EOF > "${TEMP_DIR}"/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

commonLabels:
  app.kubernetes.io/instance: springfield.csi.k8s.io
  app.kubernetes.io/part-of: csi-driver-springfield

resources:
- ./rbac.yaml
EOF

echo ${TEMP_DIR}"/kustomization.yaml"
    cat ${TEMP_DIR}"/kustomization.yaml"
    kubectl apply --kustomize "${TEMP_DIR}"

done

