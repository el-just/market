#!/bin/bash

# docker install
    sudo apt-get update
    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg2 \
        software-properties-common
    curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
    sudo add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/debian \
       $(lsb_release -cs) \
       stable"
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io

    # docker group
    sudo groupadd docker
    sudo usermod -aG docker $USER

    #docker-compose
    sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

#install yc
    curl https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash

    # yc init
    # yc container registry configure-docker
