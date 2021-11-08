#!/bin/bash

SCRIPTS_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "$SCRIPTS_DIR/build.sh"

read -p "Enter target k8s namespace [default]: " namespace
namespace=${namespace:-default}

eval $(minikube docker-env)
echo use image $IMAGE
IMAGE=$IMAGE envsubst < k8s.yaml | kubectl -n $namespace apply -f -

watch -n 1 kubectl get all
