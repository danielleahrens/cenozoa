#!/bin/bash

echo "building docker image with tag $1"
docker build /Users/dani/projects/cenozoa --platform linux/arm64 -t cenozoa:$1

echo "saving docker image to tar file"
docker save cenozoa:$1 > /tmp/cenozoa.tar
echo "MD5 sum of file:"
md5 /tmp/cenozoa.tar

echo "transferring tar file, config files and build file to pi:"
echo "transferring tar file (1 of 5):"
scp -C /tmp/cenozoa.tar ubuntu@192.168.1.10:/tmp
echo "transferring config file (2 of 5)"
scp -C /Users/dani/projects/cenozoa/application.json ubuntu@192.168.1.10:/tmp
echo "transferring config file (3 of 5)"
scp -C /Users/dani/projects/cenozoa/secrets.json ubuntu@192.168.1.10:/tmp
echo "transferring config file (4 of 5)"
scp -C /Users/dani/projects/cenozoa/nginx_config ubuntu@192.168.1.10:/tmp
echo "transferring build file (5 of 5)"
scp -C /Users/dani/projects/cenozoa/build-server.sh ubuntu@192.168.1.10:/tmp
