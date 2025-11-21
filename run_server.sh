#!/usr/bin/env bash
export PYTHONPATH=$PWD/src
. .venv/bin/activate
python -m uvicorn synapse_ws.server:app --reload --host 127.0.0.1 --port 8000
