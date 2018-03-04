#!/bin/sh
sudo docker stop $(docker ps -aq)
sudo docker rm $(docker ps -aq)
sudo docker build -t jobchain-docker .
sudo docker run -it --name jchain jobchain-docker
