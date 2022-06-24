#!/bin/bash

echo "fetching most recent repository changes..."
cd /root/GitHub/mlh-fellowship-project/app
git fetch && git reset origin/main --hard

echo "activating virtual environment..."
source /root/GitHub/mlh-fellowship-project/python3-virtualenv/bin/activate
pip3 install -r /root/GitHub/mlh-fellowship-project/requirements.txt

systemctl restart myportfolio
systemctl status myportfolio
