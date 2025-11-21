import asyncio
import json
import uuid
from typing import Any, Dict
import websockets
from .protocol import dumps_request, loads_response, RPCRequest, RPCResponse


class WSConnectionManager:
	"""Manage a single persistent WebSocket and allow multiple concurrent RPC calls.

	It creates a background task that reads messages and resolves futures keyed by request id.
	"""
	def __init__(self, url: str):
		self.url = url
		self._ws = None
		self._reader_task = None
		self._futures: Dict[str, asyncio.Future] = {}

	async def connect(self):
		self._ws = await websockets.connect(self.url)
		self._reader_task = asyncio.create_task(self._reader())

	async def _reader(self):
		try:
			async for raw in self._ws:
				resp = loads_response(raw)
				fut = self._futures.pop(resp.id, None)
				if fut and not fut.done():
					if resp.error:
						fut.set_exception(RuntimeError(resp.error))
					else:
						fut.set_result(resp.result)
		except Exception:
			# cancel pending futures
			for f in self._futures.values():
				if not f.done():
					f.set_exception(RuntimeError("connection lost"))

	async def call(self, func: str, args: list[Any], timeout: float = 5.0) -> Any:
		if self._ws is None:
			await self.connect()
		req_id = str(uuid.uuid4())
		req = RPCRequest(id=req_id, op="call", func=func, args=args)
		fut = asyncio.get_event_loop().create_future()
		self._futures[req_id] = fut
		await self._ws.send(dumps_request(req))
		return await asyncio.wait_for(fut, timeout)

	async def close(self):
		if self._ws:
			await self._ws.close()
		if self._reader_task:
			self._reader_task.cancel()