# protocol.py
from __future__ import annotations
from typing import Any, List, Optional
from pydantic import BaseModel, ValidationError
import json


class RPCRequestModel(BaseModel):
    id: str
    op: str  # e.g., "call"
    func: str
    args: List[Any] = []


class RPCResponseModel(BaseModel):
    id: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None


# Helpers to serialize / deserialize JSON strings


def dumps_request(req: RPCRequestModel) -> str:
    return req.model_dump_json()


def loads_request(raw: str) -> RPCRequestModel:
    return RPCRequestModel.model_validate_json(raw)


def dumps_response(resp: RPCResponseModel) -> str:
    return resp.model_dump_json()


def loads_response(raw: str) -> RPCResponseModel:
    return RPCResponseModel.model_validate_json(raw)


# Convenience dataclass-like wrappers (if you prefer the old names)
RPCRequest = RPCRequestModel
RPCResponse = RPCResponseModel
