#!/bin/bash
set -e

tagname=${1:-latest}
TAG=model-serving:$tagname

# copy required files/folder to a temporary container
mkdir -p build/.serving_tmp
mkdir -p build/.serving_tmp/model_training
cp -R -n ./serving build/.serving_tmp/
# add preprecessing.py as the pickled model needs it
cp -n ./model_training/preprocessing.py build/.serving_tmp/model_training/

docker build -t $TAG -f ./build/Dockerfile_serving build

# delete the temp directory
rm -rf build/.serving_tmp