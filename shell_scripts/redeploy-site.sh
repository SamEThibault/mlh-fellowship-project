#!/bin/bash

echo "fetching most recent repository changes..."
cd /root/github/mlh-fellowship-project
git checkout deployment && git pull

echo "Spinning down existing containers to conserve memory..."
sudo docker-compose -f docker-compose.home.yml down

echo "Re-building and spinning up application..."
sudo docker-compose -f docker-compose.home.yml up -d --build

