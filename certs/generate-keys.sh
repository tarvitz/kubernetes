#!/bin/bash

# see env.sh
source ./env.sh

echo "generate ca-key.pem and ca.pem"
if [[ -f ca-key.pem && ca.pem && ca.csr ]]; then
    echo "already generated, skipping"
else
    cfssl gencert -initca ca-csr.json | cfssljson -bare ca
fi

echo "generate admin-key.pem and admin.pem"
if [[ -f admin-key.pem && admin.pem && admin.csr ]]; then
    echo "already generated, skipping"
else
    cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json \
            -profile=kubernetes admin-csr.json | cfssljson -bare admin
fi

#for i in `seq $INSTANCES`; do
for idx in ${!EXTERNAL_IPS[*]}; do
  #: skip 0 index
  if [ $idx -eq 0 ]; then
    continue
  fi
  _instance=node-${idx}
  if [[ -f ${_instance}-csr.json ]]; then
    echo "keys for instance \"${_instance}\" already generated, skipping .."
  else
  cat > ${_instance}-csr.json <<EOF
{
  "CN": "system:node:${_instance}",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "RU",
      "L": "Moscow",
      "O": "system:nodes",
      "OU": "Infrastructure Unit",
      "ST": "Moscow"
    }
  ]
}
EOF

  EXTERNAL_IP=${EXTERNAL_IPS[$idx]}
  INTERNAL_IP=${INTERNAL_IPS[$idx]}
  NODE_NAME=${NODE_NAMES[$idx]}

  echo node name: ${NODE_NAME}
  echo node internal name: node-${idx}
  echo node external ip: $EXTERNAL_IP
  echo node internal ip: $INTERNAL_IP

  cfssl gencert \
      -ca=ca.pem \
      -ca-key=ca-key.pem \
      -config=ca-config.json \
      -hostname=${NODE_NAME},${_instance},${EXTERNAL_IP},${INTERNAL_IP} \
      -profile=kubernetes \
      ${_instance}-csr.json | cfssljson -bare ${_instance}

fi
done

echo "generating kube-controller-manager-key.pem and kube-controller-manager.pem"
if [[ -f kube-controller-manager.pem && kube-controller-manager-key.pem ]]; then
    echo "already generated, skipping .."
else
  cfssl gencert \
    -ca=ca.pem \
    -ca-key=ca-key.pem \
    -config=ca-config.json \
    -profile=kubernetes \
    kube-controller-manager-csr.json | cfssljson -bare kube-controller-manager

fi

echo "generating kube-proxy.pem and kube-proxy-key.pem"
if [[ -f kube-proxy-key.pem && kube-proxy.pem ]]; then
    echo "already generated, skippig .."
else
  cfssl gencert \
    -ca=ca.pem \
    -ca-key=ca-key.pem \
    -config=ca-config.json \
    -profile=kubernetes \
     kube-proxy-csr.json | cfssljson -bare kube-proxy
fi

echo "generating kube-scheduler.pem and kube-scheduler-key.pem"
if [[ -f kube-scheduler-key.pem && kube-scheduler.pem ]]; then
    echo "already generated, skippig .."
else
  cfssl gencert \
    -ca=ca.pem \
    -ca-key=ca-key.pem \
    -config=ca-config.json \
    -profile=kubernetes \
    kube-scheduler-csr.json | cfssljson -bare kube-scheduler
fi

echo "generating kube-api keys: kubernetes-key.pem and kubernetes.pem"
if [[ -f kubernetes-key.pem && kubernetes.pem ]]; then
    echo "already generated, skippig .."
else

  #: 10.32.0.1 is for default kuberentes service
  cfssl gencert \
    -ca=ca.pem \
    -ca-key=ca-key.pem \
    -config=ca-config.json \
    -hostname=10.32.0.1,${KUBE_API_SERVER_PUBLIC_ADDRESS},178.79.158.143,127.0.0.1,w40k.net,kubernetes.default,cluster.local \
    -profile=kubernetes \
    kubernetes-csr.json | cfssljson -bare kubernetes
fi


echo "generating service account keys: service-account-key.pem and service-account.pem"
if [[ -f service-account-key.pem && service-account.pem ]]; then
    echo "already generated, skippig .."
else
  cfssl gencert \
    -ca=ca.pem \
    -ca-key=ca-key.pem \
    -config=ca-config.json \
    -profile=kubernetes \
     service-account-csr.json | cfssljson -bare service-account
fi

if [[ `id -u` = 0 ]]; then
    echo "change group for certs"
    find . -iname \*.pem -exec chown root:kube {} +
    find . -iname \*.pem -exec chmod g+r {} +
fi
