# tests/test_e2e.py
import asyncio
import socket
import threading
import uvicorn
import pytest
from synapse_ws.server import app
from synapse_ws.client import call_server_function


def find_free_port() -> int:
    """Acquire a free TCP port from the OS and return it."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_for_port(host: str, port: int, timeout: float = 20.0, interval: float = 0.1) -> bool:
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
    port = find_free_port()

    # Start uvicorn in a background daemon thread and handle SystemExit gracefully
    def run_server():
        try:
            uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")
        except SystemExit:
            # uvicorn may call sys.exit() internally on error; swallow it here
            return
        except Exception:
            # In case of other exceptions, avoid propagating to test runner thread
            return

    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    # Wait for the TCP port to be ready (robust on CI)
    ready = _wait_for_port("127.0.0.1", port, timeout=20.0, interval=0.1)
    assert ready, f"Server did not become ready on port {port} in time"

    # short stable delay to let FastAPI finish internal startup
    await asyncio.sleep(0.1)

    # Use a longer RPC timeout so slow CI hosts don't cause a failure
    ws_url = f"ws://127.0.0.1:{port}/ws"
    res = await call_server_function("add_numbers", [4, 5], url=ws_url, timeout=15.0)
    assert res == 9
