kubectl delete all --all-namespaces -l app.kubernetes.io/instance=springfield.csi.k8s.io,app.kubernetes.io/part-of=csi-driver-springfield --wait=true
kubectl delete role,clusterrole,rolebinding,clusterrolebinding,serviceaccount,storageclass,csidriver --all-namespaces -l app.kubernetes.io/instance=springfield.csi.k8s.io,app.kubernetes.io/part-of=csi-driver-springfield --wait=true
