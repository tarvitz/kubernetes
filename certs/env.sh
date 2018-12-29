INSTANCES=${1:-"2"}

#: kube cluster name
CLUSTER_NAME="w40k.net"

KUBE_API_SERVER_PUBLIC_ADDRESS="178.79.168.130"
EXTERNAL_IPS=([0] "178.79.168.130" "178.79.158.143")
#: how should be node exposed, taken from their `hostname` so don't change it
#: as far as you will have a risk loose port-forward authentication x509
NODE_NAMES=([0] "w40k.net" "docker.grart.net")
INTERNAL_IPS=([0] "10.240.0.1" "10.240.1.1")

