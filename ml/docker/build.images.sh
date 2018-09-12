#!/bin/sh
@echo off

echo "Deleting docker image(s), press any key to continue, or ctrl-c to terminate"
read -p "press any key to continue"
docker image rm faisalthaheem/lt-rest:1.0

# delete stale scripts
echo "Cleaning \"scripts\" directory, press any key to continue, or ctrl-c to terminate"
read -p "press any key to continue"
rm -f ./scripts/*.py
mkdir -p ./scripts/dummy

# copy the latest scripts
echo "Copying latest scripts from jupyter..."
cp ../jupyter/*.py ./scripts/

# build docker images
echo "Building images..."
#docker build -t faisalthaheem/lt-base:1.0 -f Dockerfile.base .
docker build -t faisalthaheem/lt-base-ubuntu16:1.0 -f Dockerfile.ubuntu16.04.base .
docker build -t faisalthaheem/lt-rest:1.0 -f Dockerfile.rest .

echo "Done."
