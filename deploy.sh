#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd ~/portofolio/backend #helloworld
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin
docker stop flask-portofolio
docker rm flask-portofolio
docker rmi -f agungajin19/container:BE2
docker run -d --name flask-portofolio -p 5000:5000 agungajin19/container:BE2