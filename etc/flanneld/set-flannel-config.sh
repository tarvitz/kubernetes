#!/bin/bash
config=${1:-"flannel-config.json"}
ETCDCTL_CA_FILE='/var/lib/kubernetes/ca.pem' \
ETCDCTL_CERT_FILE='/var/lib/kubernetes/kubernetes.pem' \
ETCDCTL_KEY_FILE='/var/lib/kubernetes/kubernetes-key.pem' \
ETCDCTL_ENDPOINTS='https://127.0.0.1:2379' \
\
etcdctl set /coreos.com/network/config < ./${config}
