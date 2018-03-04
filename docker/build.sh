#!/bin/sh
sudo docker stop $(docker ps -aq)
sudo docker rm $(docker ps -aq)
sudo docker build -t jobchain-docker .
sudo docker run -it --env-file=.env --name jchain jobchain-docker
