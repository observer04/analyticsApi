#!/usr/bin/env bash
set -e

# activate venv
[ -f /opt/venv/bin/activate ] && source /opt/venv/bin/activate

# where main.py lives
cd /code

RUN_HOST=${HOST:-0.0.0.0}
RUN_PORT=${PORT:-8000}


exec gunicorn -k uvicorn.workers.UvicornWorker \
     --bind "${RUN_HOST}:${RUN_PORT}" \
     main:app