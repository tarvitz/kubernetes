
source ./env.sh

[[ ! -d kubeconfig ]] && mkdir kubeconfig

echo "generate kubelet configurations"
#for i in `seq $INSTANCES`; do
for idx in ${!EXTERNAL_IPS[*]}; do
  if [ $idx -eq 0 ]; then
    continue
  fi

  instance=node-${idx}
  if [[ -f kubeconfig/${instance}.kubeconfig ]]; then
    echo "kubeconfig/${instance}.kubeconfig generated, skipping .."
  else
  kubectl config set-cluster ${CLUSTER_NAME} \
    --certificate-authority=ca.pem \
    --embed-certs=true \
    --server=https://${KUBE_API_SERVER_PUBLIC_ADDRESS}:6443 \
    --kubeconfig=kubeconfig/${instance}.kubeconfig

  kubectl config set-credentials system:node:${instance} \
    --client-certificate=${instance}.pem \
    --client-key=${instance}-key.pem \
    --embed-certs=true \
    --kubeconfig=kubeconfig/${instance}.kubeconfig

  kubectl config set-context default \
    --cluster=${CLUSTER_NAME} \
    --user=system:node:${instance} \
    --kubeconfig=kubeconfig/${instance}.kubeconfig

  kubectl config use-context default --kubeconfig=kubeconfig/${instance}.kubeconfig
  fi
done

echo "generate kube-proxy configuration"
if [[ -f kubeconfig/kube-proxy.kubeconfig ]]; then
    echo "kubeconfig/kube-proxy.kubeconfig generated, skipping .."
else
  kubectl config set-cluster ${CLUSTER_NAME} \
    --certificate-authority=ca.pem \
    --embed-certs=true \
    --server=https://${KUBE_API_SERVER_PUBLIC_ADDRESS}:6443 \
    --kubeconfig=kubeconfig/kube-proxy.kubeconfig

  kubectl config set-credentials system:kube-proxy \
    --client-certificate=kube-proxy.pem \
    --client-key=kube-proxy-key.pem \
    --embed-certs=true \
    --kubeconfig=kubeconfig/kube-proxy.kubeconfig

  kubectl config set-context default \
    --cluster=${CLUSTER_NAME} \
    --user=system:kube-proxy \
    --kubeconfig=kubeconfig/kube-proxy.kubeconfig

  kubectl config use-context default --kubeconfig=kubeconfig/kube-proxy.kubeconfig
fi


echo "generate kube-controller-manager kubeconfig configuration"
if [[ -f kubeconfig/kube-controller-manager.kubeconfig ]]; then
    echo "kubeconfig/kube-controller-manager.kubeconfig already generated, skipping .."
else
  kubectl config set-cluster ${CLUSTER_NAME} \
    --certificate-authority=ca.pem \
    --embed-certs=true \
    --server=https://${KUBE_API_SERVER_PUBLIC_ADDRESS}:6443 \
    --kubeconfig=kubeconfig/kube-controller-manager.kubeconfig

  kubectl config set-credentials system:kube-controller-manager \
    --client-certificate=kube-controller-manager.pem \
    --client-key=kube-controller-manager-key.pem \
    --embed-certs=true \
    --kubeconfig=kubeconfig/kube-controller-manager.kubeconfig

  kubectl config set-context default \
    --cluster=${CLUSTER_NAME} \
    --user=system:kube-controller-manager \
    --kubeconfig=kubeconfig/kube-controller-manager.kubeconfig

  kubectl config use-context default --kubeconfig=kubeconfig/kube-controller-manager.kubeconfig
fi

echo "generate kube-scheduler kubeconfig configuration"
if [[ -f kubeconfig/kube-scheduler.kubeconfig ]]; then
    echo "kubeconfig/kube-scheduler.kubeconfig already generated, skipping .."v
else
  kubectl config set-cluster ${CLUSTER_NAME} \
    --certificate-authority=ca.pem \
    --embed-certs=true \
    --server=https://${KUBE_API_SERVER_PUBLIC_ADDRESS}:6443 \
    --kubeconfig=kubeconfig/kube-scheduler.kubeconfig

  kubectl config set-credentials system:kube-scheduler \
    --client-certificate=kube-scheduler.pem \
    --client-key=kube-scheduler-key.pem \
    --embed-certs=true \
    --kubeconfig=kubeconfig/kube-scheduler.kubeconfig

  kubectl config set-context default \
    --cluster=${CLUSTER_NAME} \
    --user=system:kube-scheduler \
    --kubeconfig=kubeconfig/kube-scheduler.kubeconfig

  kubectl config use-context default --kubeconfig=kubeconfig/kube-scheduler.kubeconfig
fi

echo "generate admin.kubeconfig configuration"
if [[ -f kubeconfig/admin.kubeconfig ]]; then
    echo "kubeconfig/admin.kubeconfig already generated, skipping .."
else
  kubectl config set-cluster ${CLUSTER_NAME} \
    --certificate-authority=ca.pem \
    --embed-certs=true \
    --server=https://${KUBE_API_SERVER_PUBLIC_ADDRESS}:6443 \
    --kubeconfig=kubeconfig/admin.kubeconfig

  kubectl config set-credentials admin \
    --client-certificate=admin.pem \
    --client-key=admin-key.pem \
    --embed-certs=true \
    --kubeconfig=kubeconfig/admin.kubeconfig

  kubectl config set-context default \
    --cluster=${CLUSTER_NAME} \
    --user=admin \
    --kubeconfig=kubeconfig/admin.kubeconfig

  kubectl config use-context default --kubeconfig=kubeconfig/admin.kubeconfig
fi

#: EXTRA
echo "generate coredns.kubeconfig configuration"
if [[ -f kubeconfig/coredns.kubeconfig ]]; then
    echo "kubeconfig/coredns.kubeconfig already generated, skipping .."
else
  kubectl config set-cluster ${CLUSTER_NAME} \
    --certificate-authority=ca.pem \
    --embed-certs=true \
    --server=https://${KUBE_API_SERVER_PUBLIC_ADDRESS}:6443 \
    --kubeconfig=kubeconfig/coredns.kubeconfig

  kubectl config set-credentials system:coredns \
    --client-certificate=admin.pem \
    --client-key=admin-key.pem \
    --embed-certs=true \
    --kubeconfig=kubeconfig/coredns.kubeconfig

  kubectl config set-context default \
    --cluster=${CLUSTER_NAME} \
    --user=system:coredns \
    --kubeconfig=kubeconfig/coredns.kubeconfig

  kubectl config use-context default --kubeconfig=kubeconfig/coredns.kubeconfig
fi

echo "generate flanneld.kubeconfig configuration"
if [[ -f kubeconfig/flanneld.kubeconfig ]]; then
    echo "kubeconfig/flanneld.kubeconfig already generated, skipping .."
else
  kubectl config set-cluster ${CLUSTER_NAME} \
    --certificate-authority=ca.pem \
    --embed-certs=true \
    --server=https://${KUBE_API_SERVER_PUBLIC_ADDRESS}:6443 \
    --kubeconfig=kubeconfig/flanneld.kubeconfig

  kubectl config set-credentials system:flanneld \
    --client-certificate=admin.pem \
    --client-key=admin-key.pem \
    --embed-certs=true \
    --kubeconfig=kubeconfig/flanneld.kubeconfig

  kubectl config set-context default \
    --cluster=${CLUSTER_NAME} \
    --user=system:flanneld \
    --kubeconfig=kubeconfig/flanneld.kubeconfig

  kubectl config use-context default --kubeconfig=kubeconfig/flanneld.kubeconfig
fi

if [[ `id -u` = 0 ]]; then
  find kubeconfig -type f -exec chown root:kube {} +
fi
find kubeconfig -type f -exec chmod g+r {} +
