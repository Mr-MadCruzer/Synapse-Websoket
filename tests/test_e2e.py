# tests/test_e2e.py
import asyncio
import socket
import threading
import uvicorn
import pytest
from synapse_ws.server import app
from synapse_ws.client import call_server_function

def _wait_for_port(host: str, port: int, timeout: float = 15.0, interval: float = 0.1) -> bool:
    """
    Poll until a TCP connection to (host, port) succeeds or timeout is reached.
    Returns True if port became connectable, False otherwise.
    """
    deadline = asyncio.get_event_loop().time() + timeout
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except Exception:
            if asyncio.get_event_loop().time() > deadline:
                return False
            # synchronous short sleep using asyncio loop to be compatible in pytest-asyncio
            asyncio.get_event_loop().run_until_complete(asyncio.sleep(interval))


@pytest.mark.asyncio
async def test_e2e():
    # Start uvicorn in a background thread
    def run_server():
        # Using uvicorn.run is fine for tests; it will block the thread but not the test thread.
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    # Wait for the TCP port to be ready (robust on CI)
    ready = _wait_for_port("127.0.0.1", 8000, timeout=20.0, interval=0.1)
    assert ready, "Server did not become ready in time"

    # give FastAPI a brief moment to finish internal startup if necessary
    await asyncio.sleep(0.2)

    # Use a longer timeout for the RPC call so slow CI hosts don't cause a test failure
    res = await call_server_function("add_numbers", [4, 5], url="ws://127.0.0.1:8000/ws", timeout=15.0)
    assert res == 9
    # Note: The server thread will be killed when the test process exits.