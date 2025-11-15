#!/usr/bin/env bash

set -euo pipefail

echo "Checking for existing oracle db image"
[ -z $(docker image ls | grep oracle) ] && echo "No image found. Pulling from registry" && docker pull container-registry.oracle.com/database/free:latest
echo "Checking for existing oracle db container"
if [ -n "$(docker ps -a | grep oracle-db)" ]; then echo "Found a running container. Killing and restarting..." && docker stop oracle-db && docker rm oracle-db; fi
docker run -p 1521:1521 -d --name oracle-db container-registry.oracle.com/database/free:latest
while ! docker ps --filter "name=oracle-db" --format '{{.Status}}' | grep -q 'healthy'; do
    echo "Waiting for db container to start accepting connections..."
    sleep 3
done
docker exec oracle-db ./setPassword.sh helloworld