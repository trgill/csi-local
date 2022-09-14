DEPLOYMENT_FILE_PATH="./test.yaml"
RELEASE_NAME=springfield-csi-driver

helm template $RELEASE_NAME ../helm/springfield-csi-driver --namespace springfield-csi --set > $DEPLOYMENT_FILE_PATH

echo "Deployment file $DEPLOYMENT_FILE_PATH ready"

echo "Building Helm Package"

helm package springfield-csi-driver --destination helm_out/
