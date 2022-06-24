#!/bin/bash

echo "fetching most recent repository changes..."
cd /home/GitHub/mlh-fellowship-project/app
git fetch && git reset origin/main --hard

echo "activating virtual environment..."
source /home/GitHub/mlh-fellowship-project/python3-virtualenv/bin/activate
pip3 install -r /home/GitHub/mlh-fellowship-project/requirements.txt

systemctl restart myportfolio
systemctl status myportfolio
