#!/bin/bash
rm -f node-*.json *.csr *.pem

if [[ ! -z $1 && $1 = 'all' ]]; then
    rm -f kubeconfig/*
fi
