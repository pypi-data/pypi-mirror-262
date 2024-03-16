from typing import Any, TYPE_CHECKING, Optional, Callable, Union
from typing_extensions import TypeAlias
from pydantic import BaseModel, TypeAdapter
from fastapi import WebSocket
from dataclasses import asdict

from .client_types import HandshakePackage, ClientPackageTypes

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

PackageHandlerFallback: TypeAlias = Callable[[Exception, WebSocket], Union[None, Any]]
async def package_handler(ws: WebSocket, *, fallback: Optional[PackageHandlerFallback] = None):
    """处理客户端信息并转换为包"""
    try:
        return dict2pkg(await ws.receive_json())
    except RuntimeError:
        raise WSCloseException
    except Exception as e:
        # 若 fallback 为 None 或 其返回值 为 None, 则直接返回错误
        return (fallback(e, ws) if fallback is not None else e) or e

class SkipHandlerExcpetion(Exception):
    pass

class WSCloseException(Exception):
    def __init__(self, code: int=1003, msg: str ='') -> None:
        self.code = code
        self.msg = msg

def dict2pkg(received: dict):
    return TypeAdapter(ClientPackageTypes).validate_python(received, strict=True)

async def send_json(ws: WebSocket, jsonable: dict, **kwargs):
    try:
        await ws.send_json(jsonable, **kwargs)
    except RuntimeError:  # 客户端关闭
        raise WSCloseException

async def send_pydantic_model(ws: WebSocket, model: BaseModel, **kwargs):
    await send_json(ws, model.model_dump(**kwargs))

async def send_dataclass(ws: WebSocket, dc: 'DataclassInstance', **kwargs):
    await send_json(ws, asdict(dc), **kwargs)
