INSTANCES=${1:-"2"}

#: kube cluster name
CLUSTER_NAME="k8s.w40k.net"

KUBE_API_SERVER_PUBLIC_ADDRESS="178.79.148.185"
KUBE_API_SERVER_INTERNAL_ADDRESS="192.168.153.60"

EXTERNAL_IPS=([0] "178.79.168.130" "178.79.158.143")

#: how should be node exposed, taken from their `hostname` so don't change it
#: as far as you will have a risk loose port-forward authentication x509
NODE_NAMES=([0] "w40k.net" "docker.grart.net")

#: node-1, node-2 ips (by hosts)
CLUSTER_IPS=([0] "192.168.164.230" "192.168.186.196")

