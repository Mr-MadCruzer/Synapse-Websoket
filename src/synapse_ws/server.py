# server.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Any, Callable, Dict
from .protocol import RPCRequest, RPCResponse, loads_request, dumps_response

app = FastAPI(title="Synapse WS Exercise")


# -------------------------
# Business logic
# -------------------------
def add_numbers(a: float, b: float) -> float:
    """Return sum of two numbers."""
    return a + b


# Function registry
FUNCTION_REGISTRY: Dict[str, Callable[..., Any]] = {
    "add_numbers": add_numbers,
}


# -------------------------
# WebSocket endpoint
# -------------------------
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        while True:
            raw = await ws.receive_text()

            try:
                req: RPCRequest = loads_request(raw)

                if req.op != "call":
                    raise ValueError(f"Unsupported operation: {req.op}")

                func = FUNCTION_REGISTRY.get(req.func)
                if func is None:
                    resp = RPCResponse(id=req.id, error=f"Unknown function: {req.func}")
                else:
                    result = func(*req.args)
                    resp = RPCResponse(id=req.id, result=result)

            except Exception as exc:
                resp = RPCResponse(id=req.id if 'req' in locals() else None, error=str(exc))

            await ws.send_text(dumps_response(resp))

    except WebSocketDisconnect:
        return
