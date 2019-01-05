#!/bin/bash
OS=$(uname -o)
BUILD="docker build"
PTY=""

if [[ $OS == "Msys" ]]; then
    PTY="winpty"
    BUILD="${PTY} ${BUILD}"
fi

IMAGE=${IMAGE:-"nfox/k8s-example-backend"}
TAG=${TAGE:-"dev"}

${BUILD} -t ${IMAGE}:${TAG} -f Dockerfile . $@

if [[ ! -z $PUSH ]]; then
    ${PTY} docker push ${IMAGE}:${TAG}
fi
