\
        @echo off
        set PYTHONPATH=%CD%\src
        call .venv\Scripts\Activate.bat
        python -m uvicorn synapse_ws.server:app --reload --host 127.0.0.1 --port 8000
