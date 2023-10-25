#!/bin/bash

source venv/bin/activate
python3 telegram_bot/main.py &
python3 server/server.py &
python3 model/model.py &

jobs -p > pids
