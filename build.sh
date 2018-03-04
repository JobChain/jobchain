#!/bin/sh
sudo docker stop $(docker ps -aq)
sudo docker rm $(docker ps -aq)
sudo docker build -f docker/Dockerfile -t jobchain-docker .
sudo docker run -it --env-file=docker/env --name jchain jobchain-docker
