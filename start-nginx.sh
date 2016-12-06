#!/usr/bin/env bash
set -exuo pipefail

# configure nginx to use the local nginx config and relative paths
sudo nginx -c $(pwd)/nginx/nginx.conf -p "$(pwd)/nginx"
