#!/bin/bash
# To be run on AWS EC2
# running Amazon linux OS
set -euo pipefail

#install
sudo yum install -y git
sudo yum install docker -y
sudo yum install -y libxcrypt-compat
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo usermod -aG docker ec2-user
newgrp docker
sudo systemctl start docker
sudo systemctl enable docker  # optional, starts on boot

#checkout the repo and unzip the data to where it needs to be
git clone https://github.com/elvinpoole/carms-program-api.git
git clone https://github.com/dnokes/Junior-Data-Scientist.git
unzip Junior-Data-Scientist/1503_program_descriptions_x_section.zip -d carms-program-api/data/
cd carms-program-api/

docker-compose up --build -d