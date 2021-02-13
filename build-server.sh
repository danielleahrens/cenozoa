#!/bin/bash

echo "md5 of tar file:"
md5sum /tmp/cenozoa.tar

echo "updating config files"
echo "moving file from /tmp to /opt/cenozoa 1 of 3"
mv /tmp/application.json /opt/cenozoa
echo "moving file from /tmp to /opt/cenozoa 2 of 3"
mv /tmp/secrets.json /opt/cenozoa
echo "moving file from /tmp to /opt/cenozoa 3 of 3"
mv /tmp/nginx_config /opt/cenozoa

echo "loading docker image from tar file"
docker load < cenozoa.tar

echo "removing then running cenozoa docker container"
echo "docker kill"
docker kill cenozoa
echo "docker rm"
docker rm cenozoa
echo "docker run"
docker run -v /opt/cenozoa/application.json:/cenozoa/application.json -v /opt/cenozoa/secrets.json:/cenozoa/secrets.json -e CONFIG_PATH=/cenozoa/application.json -e SECRETS_PATH=/cenozoa/secrets.json --network=cenozoanet --name=cenozoa --rm -d cenozoa:$1

echo "running nginx docker container"
echo "docker kill"
docker kill nginx
echo "docker rm"
docker rm nginx
echo "docker run"
docker run -v /opt/cenozoa/nginx_config:/etc/nginx/conf.d/default.conf -v /opt/cenozoa/.htpasswd:/etc/apache2/.htpasswd -v /opt/cenozoa/.supasswd:/etc/apache2/.supasswd -p 80:80 --network=cenozoanet --name=nginx --rm -d nginx
