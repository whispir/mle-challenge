#!/bin/bash

git_hash=$(git log --pretty=format:'%h' -n 1)
echo $git_hash

read -p "Enter docker image tag name [${git_hash}]: " tag
tag=${tag:-$git_hash}
echo -e build image with name:  "\e[31mruodingt7/wml:$tag\e[0m"

read -p "Proceed?" confirm


docker build -t ruodingt7/wml:$tag .
docker push ruodingt7/wml:$tag
#docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]

