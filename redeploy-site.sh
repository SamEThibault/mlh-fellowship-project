#!/bin/bash

echo "killing existing tmux sessions..."
tmux kill-server

#this ensures port:80 is not in use since we want to host the site through the default http port
sudo fuser -n tcp -k 80

echo "fetching most recent repository changes..."
cd /home/GitHub/mlh-fellowship-project/app
git fetch && git reset origin/main --hard

echo "activating virtual environment..."
source /home/GitHub/mlh-fellowship-project/python3-virtualenv/bin/activate
pip3 install -r /home/GitHub/mlh-fellowship-project/requirements.txt

echo "starting tmux session..."
cd /home/GitHub/mlh-fellowship-project/app
tmux new-session -d -s flask_portfolio 'source /home/GitHub/mlh-fellowship-project/python3-virtualenv/bin/activate && export FLASK_APP=__init__.py && export FLASK_RUN_PORT=80 && flask run --host=0.0.0.0; $SHELL'

echo "current tmux sessions:"
tmux ls
echo "flask application started"
echo "Complete"

