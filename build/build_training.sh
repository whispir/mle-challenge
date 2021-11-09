#!/bin/bash
set -e

tagname=${1:-latest}
TAG=model-training:$tagname

# copy required files/folder to a temporary container
mkdir -p build/.container
cp -n run_training.py build/.container/
cp -R -n ./data build/.container/
cp -R -n ./model_training build/.container/

docker build -t $TAG -f ./build/Dockerfile_training build

# delete the temp container directory
rm -rf build/.container

