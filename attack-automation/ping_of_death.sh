#!/usr/bin/env bash

set -x

server="35.247.20.4"

sudo apt-get install hping3
sudo hping3 -d 65500 --icmp $server

set +x
