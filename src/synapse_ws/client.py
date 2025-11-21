# client.py
import asyncio
import json
import uuid
from typing import Any, List
import websockets

from .protocol import (
    RPCRequestModel,
    RPCResponseModel,
    dumps_request,
    loads_response,
)

DEFAULT_WS_URL = "ws://127.0.0.1:8000/ws"


async def call_server_function(func: str, args: List[Any], url: str = DEFAULT_WS_URL, timeout: float = 5.0) -> Any:
    """Generic RPC client wrapper."""
    req_id = str(uuid.uuid4())
    req = RPCRequestModel(id=req_id, op="call", func=func, args=args)

    async with websockets.connect(url) as ws:
        await ws.send(dumps_request(req))

        raw = await asyncio.wait_for(ws.recv(), timeout)
        resp = loads_response(raw)

        if resp.error:
            raise RuntimeError(resp.error)

        return resp.result


async def call_add_numbers(a: float, b: float, url: str = DEFAULT_WS_URL) -> float:
    """Specific wrapper for add_numbers RPC."""
    return await call_server_function("add_numbers", [a, b], url=url)
