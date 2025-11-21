.PHONY: install run test lint
install:
	python -m venv .venv
	. .venv/bin/activate; python -m pip install --upgrade pip
	. .venv/bin/activate; python -m pip install -r requirements.txt

run:
	. .venv/bin/activate; python -m uvicorn synapse_ws.server:app --reload --host 127.0.0.1 --port 8000

test:
	. .venv/bin/activate; python -m pytest -q

lint:
	. .venv/bin/activate; python -m pip install ruff black
	. .venv/bin/activate; ruff src tests examples
	. .venv/bin/activate; black src tests examples
