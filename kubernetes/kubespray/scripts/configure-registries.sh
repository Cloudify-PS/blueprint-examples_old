#!/usr/bin/env bash

echo "{ \"insecure-registries\":[\"${CLOUDIFY_MANAGER_IP}:5000\"] }" | sudo tee /etc/docker/daemon.json
sudo service docker restart 
