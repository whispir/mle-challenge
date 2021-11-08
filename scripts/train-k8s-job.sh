#!/bin/bash

git_hash=$(git log --pretty=format:'%h' -n 1)
echo $git_hash

read -p "Enter docker image tag name [${git_hash}]: " tag

tag=${tag:-$git_hash}

IMAGE=$(echo ruodingt7/wml:$tag)

echo $IMAGE
echo -e build image with name:  "\e[31m$IMAGE\e[0m"

docker build -t $IMAGE .

read -p "Enter target k8s namespace [default]: " namespace
namespace=${namespace:-default}

eval $(minikube docker-env)
echo use image $IMAGE
IMAGE=$IMAGE envsubst < k8s-train-job.yaml | kubectl -n $namespace apply -f -

watch -n 1 kubectl get all
