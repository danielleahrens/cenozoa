# cenozoa
A flask web app for IOT sensors and other devices.

## Deploying instructions

### This app runs on a raspberry pi in a docker container. Because the raspberry pi has an ARM processor (and not a x86 as the mac has), use this build command:

`cd` into the project directory

`docker build . --platform linux/arm64 -t cenozoa:{additional tags here}`

### Next transfer the docker image to the raspberry pi:

#### Save the docker image as a tar file, preferably in a `tmp` directory or similar:
`docker save cenozoa cenozoa.tar`

#### Secure copy the file to the pi, the -C flag compresses the file.
`scp -C cenozoa.tar ubuntu@{ip address}:/tmp`

#### ssh onto the pi and assume root privileges or add sudo to the command, `cd` to the `/tmp` directory:
`docker load < cenozoa.tar`

### If this is a fresh raspberry pi, before running the docker container create a docker network so this container and the nginx container will be able to communicate:
`docker network create cenozoanet`

### Run the docker container:
#### -v sets the config file on the pi to a location accessible in the container, -e sets an environment variable which specifies the file path to the config file, --network specifies to use the docker network created above, --rm will remove the docker container after its terminated (this is required because the container was given a --name), -d so it continues running after exiting ssh session:
`docker run -v /opt/cenozoa/application.json:/cenozoa/application.json /opt/cenozoa/secrets.json:/cenozoa/secrets.json -e CONFIG_PATH=/cenozoa/application.json SECRETS_PATH=/cenozoa/secrets.json --network=cenozoanet --name=cenozoa --rm -d cenozoa`

### After getting the cenozoa container running, start the nginx container:
#### cenozoa must be running prior to running the nginx container, flags perform similar functions as mentioned above, -p binds the container's port 80 to the pi's port 80:
`docker run -v /opt/cenozoa/nginx_config:/etc/nginx/conf.d/default.conf -p 80:80 --network=cenozoanet --name=nginx --rm -d nginx`

### If the necessary files aren't in the `/opt/cenozoa` directory on the pi, or if they've been updated on your local machine:
`scp application.json ubuntu@{ip address}:/tmp`
\n or \n 
`scp secrets.json ubuntu@{ip address}:/tmp`
\n or \n 
`scp nginx_config ubuntu@{ip address}:/tmp`

#### Then ssh onto pi and move file from /tmp to /opt/cenozoa, root privleges will be required:
`mv application.json /opt/cenozoa`
\n or \n
`mv secrets.json /opt/cenozoa`
\n or \n
`mv nginx_config /opt/cenozoa`

