#: kube cluster name (api-master fqdn)
CLUSTER_NAME="k8s.w40k.net"

#: api-master global ip address
KUBE_API_SERVER_PUBLIC_ADDRESS="178.79.148.185"
#: api-master local ip address
KUBE_API_SERVER_INTERNAL_ADDRESS="192.168.153.60"

#: NOTE NODE_NAMES, EXTERNAL_IPS and CLUSTER_IPS don't have
#: array match size validation, so please pay attention while
#: modifying configuration

#: node names, you can pick local or FQDN by your own wish
#: please note that w40k.net would be associated with node-1
#: docker.grart.net with node-2 and so on
NODE_NAMES=([0] "w40k.net" "docker.grart.net")

#: node-1, node-2 external ips
EXTERNAL_IPS=([0] "178.79.168.130" "178.79.158.143")

#: node-1, node-2 internal ips
CLUSTER_IPS=([0] "192.168.164.230" "192.168.186.196")
