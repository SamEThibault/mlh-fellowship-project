#!/bin/bash

echo "fetching most recent repository changes..."
cd /root/GitHub/mlh-fellowship-project/app
git fetch && git reset origin/main --hard

echo "Spinning down existing containers to conserve memory..."
docker compose -f docker-compose.prod.yml down

echo "Re-building and spinning up application..."
docker compose -f docker-compose.prod.yml up -d --build

