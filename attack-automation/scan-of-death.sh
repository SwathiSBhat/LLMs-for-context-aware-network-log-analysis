#!/usr/bin/env bash

set -x

server="35.247.20.4"

sudo nmap -A -Pn $server

set +x
