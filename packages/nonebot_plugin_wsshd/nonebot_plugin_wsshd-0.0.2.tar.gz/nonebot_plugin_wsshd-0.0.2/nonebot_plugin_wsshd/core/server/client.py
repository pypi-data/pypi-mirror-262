from dataclasses import asdict, is_dataclass
from pydantic import BaseModel, TypeAdapter, ConfigDict
from typing_extensions import TypeAlias, Optional, Union
from typing import Any, Literal, TYPE_CHECKING, Dict
from fastapi import WebSocket
from pydantic_core import ValidationError
from asyncio import iscoroutine

from nonebot import logger

from .shared import package_handler, PackageHandlerFallback, SkipHandlerExcpetion, send_json, send_pydantic_model, WSCloseException
from .server_types import WSServerData, WSUnknownAction, WRONG_CANNOT_HANDSHAKE, WSFailedGotRes
from .client_types import ClientTypes, ClientPackage, HandshakePackage, ActionTypes, PackageCallbackType

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

class Client(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: Optional[ClientTypes] = None
    mid: str
    ws: WebSocket
    callbacks: Dict[ActionTypes, PackageCallbackType]

    async def send_json(self, jsonable: dict, **kwargs):
        await send_json(self.ws, jsonable, **kwargs)

    async def send_pydantic_model(self, model: BaseModel, **kwargs):
        await send_pydantic_model(self.ws, model, **kwargs)
    
    async def send_dataclass(self, dc: 'DataclassInstance', **kwargs):
        await self.send_json(asdict(dc), **kwargs)

    async def send(self, response: Any):
        if is_dataclass(response):
            await self.send_dataclass(response)
            return
        elif isinstance(response, BaseModel):
            await self.send_pydantic_model(response)
            return
        else:
            await self.send_json(response)
    
    async def receive_package(self, fallback: Optional[PackageHandlerFallback] = None) -> 'ClientPackage':
        pkg = await package_handler(self.ws, fallback=fallback)
        if not isinstance(pkg, ClientPackage):
            if isinstance(pkg, ValidationError):
                await self.send(WSUnknownAction(data=pkg.errors()))
            else:
                await self.send(WSUnknownAction(data={'error': repr(pkg)}))

            raise SkipHandlerExcpetion
        
        return pkg

    async def mainloop(self):
        while True:
            try:
                pkg = await self.receive_package()
            except WSCloseException:
                break
            except SkipHandlerExcpetion:
                continue

            if pkg.action == 'handshake':
                await self.send(WRONG_CANNOT_HANDSHAKE)
                continue
            
            try:
                await self.main(pkg)
            except WSCloseException:
                break
            except SkipHandlerExcpetion:
                continue

    async def main(self, pkg: ClientPackage):
        raise NotImplemented

class NonebotClient(Client):
    type: Literal['nonebot'] = 'nonebot'

    async def main(self, pkg: ClientPackage):
        if pkg.action is None:
            raise SkipHandlerExcpetion

        try:
            res = self.callbacks.get(pkg.action, None)
            if callable(res):
                res = res(self.ws, pkg)

            if iscoroutine(res):
                res = await res
            
            if not isinstance(res, WSServerData):
                raise SkipHandlerExcpetion

            await self.send(res)
        except Exception as e:
            await self.send(WSFailedGotRes(data={'action': pkg.action, 'error': repr(e)}))
        

class KoishiClient(Client):
    type: Literal['koishi']  = 'koishi'

ClientClassTypes: TypeAlias = Union[NonebotClient, KoishiClient]
def create_client(handshake_pkg: HandshakePackage, ws: WebSocket, callbacks: Dict[ActionTypes, PackageCallbackType]) -> Client:
    data = {'type': handshake_pkg.data.type, 'mid': handshake_pkg.data.mid, 'ws': ws, 'callbacks': callbacks}

    client: Any = TypeAdapter(ClientClassTypes).validate_python(data, strict=True)
    return client
