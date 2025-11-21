# Synapse WebSocket Exercise — README

This repository contains a complete, production-ready implementation of the **Synapse WebSocket Coding Exercise**. It includes a FastAPI WebSocket server, an async Python client, a persistent connection manager, pydantic validation, tests, and CI.

---

## 📌 Project Overview

This project demonstrates your ability to:

- Build a **WebSocket server** using Python (FastAPI + Uvicorn)
- Build an **async client** using `websockets`
- Implement **RPC-style function calls** (add_numbers, etc.)
- Validate input/output using **pydantic**
- Handle errors cleanly
- Provide examples and automated tests
- Use a professional project structure

---

## 📂 Project Structure

synapse-ws-exercise/
├── src/
│ └── synapse_ws/
│ ├── init.py
│ ├── server.py
│ ├── client.py
│ ├── protocol.py
│ └── connection.py
├── examples/
│ └── demo_client.py
├── tests/
│ ├── test_unit.py
│ └── test_e2e.py
├── requirements.txt
├── pyproject.toml
├── README.md
├── run_server.bat
├── run_server.sh
└── .github/workflows/ci.yml

yaml
Copy code

---

# 🚀 Quick Start (Windows PowerShell)

### 1️⃣ Navigate to project folder
```powershell
cd D:\PYTHON\Synapse-websockets
2️⃣ Create virtual environment
powershell
Copy code
python -m venv .venv
3️⃣ Activate it
powershell
Copy code
.\.venv\Scripts\Activate.ps1
4️⃣ Install dependencies
powershell
Copy code
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
5️⃣ Set PYTHONPATH (important)
powershell
Copy code
$env:PYTHONPATH = "$PWD\src"
6️⃣ Run the WebSocket server
powershell
Copy code
python -m uvicorn synapse_ws.server:app --reload --host 127.0.0.1 --port 8000
Or using the batch script

powershell
Copy code
.\run_server.bat
➡️ Leave this running.

🟡 Running Client Demo (Second Terminal)
powershell
Copy code
cd D:\PYTHON\Synapse-websockets
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD\src"
python examples\demo_client.py
Expected Output
scss
Copy code
add_numbers(1, 2) -> 3
add_numbers(3.5, 4.5) -> 8.0
add_numbers(-1, 10) -> 9
🧪 Running Tests
powershell
Copy code
python -m pytest -q
Expected:

Copy code
2 passed
🧠 How It Works
Server
FastAPI WebSocket endpoint: /ws

Uses a function registry (mapping strings → functions)

Validates messages using pydantic

Responds using { id, result, error }

Client
Uses Python websockets package

Sends JSON RPC requests

Waits for responses by ID

Includes helper: call_add_numbers(a, b)

Protocol
Schema defined in protocol.py

Models:

RPCRequestModel

RPCResponseModel

Persistent Connection (optional)
connection.py includes WSConnectionManager

Supports:

Reconnect

Multiple parallel RPC calls

Response routing by request ID

🧰 Tools Used
Python 3.10+

FastAPI (server)

Uvicorn (ASGI server)

Websockets (client)

Pydantic (validation)

Pytest (testing)

GitHub Actions (CI)

Makefile / batch / shell scripts

📝 Example RPC Message
Client request:
json
Copy code
{
  "id": "1234",
  "op": "call",
  "func": "add_numbers",
  "args": [5, 10]
}
Server response:
json
Copy code
{
  "id": "1234",
  "result": 15,
  "error": null
}
🧯 Troubleshooting
🔹 ModuleNotFoundError: synapse_ws
Run:

powershell
Copy code
$env:PYTHONPATH = "$PWD\src"
🔹 IndentationError
Open file in VS Code → NOT Notepad.

🔹 Server cannot import module
You are running the command from the wrong directory.
Run everything from the project root.