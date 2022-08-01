#!/bin/bash

echo "fetching most recent repository changes..."
cd /root/github/mlh-fellowship-project
git fetch && git reset origin/main --hard

echo "Spinning down existing containers to conserve memory..."
docker compose -f docker-compose.home.yml down

echo "Re-building and spinning up application..."
docker compose -f docker-compose.home.yml up -d --build

