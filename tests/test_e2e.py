import asyncio
import threading
import uvicorn
import pytest
from synapse_ws.server import app
from synapse_ws.client import call_add_numbers


@pytest.mark.asyncio
async def test_e2e():
def run_server():
uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")


t = threading.Thread(target=run_server, daemon=True)
t.start()
await asyncio.sleep(0.5)
res = await call_add_numbers(4, 5)
assert res == 9