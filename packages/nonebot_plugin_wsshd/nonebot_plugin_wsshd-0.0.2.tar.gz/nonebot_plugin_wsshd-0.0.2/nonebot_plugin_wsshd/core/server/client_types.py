from typing_extensions import TypeAlias, Coroutine
from typing import Literal, Optional, Any, Union, Callable
from pydantic import BaseModel
from fastapi import WebSocket

from .server_types import WSServerData

ClientTypes: TypeAlias = Literal['nonebot', 'koishi']

ActionTypes: TypeAlias = Literal['handshake', 'send/private', 'send/group', 'send/channel', 'debug/test', 'bot/all']
PackageCallbackType: TypeAlias = Optional[Union[WSServerData, Callable[[WebSocket, 'ClientPackage'], Union[WSServerData, Coroutine[Any, Any, WSServerData]]]]]

class ClientPackage(BaseModel):
    action: Optional[ActionTypes] = None  # None is unkonwn
    data: Any = None

class HandshakeData(BaseModel):
    type: ClientTypes
    username: str
    password: str  # 已加密的 password
    mid: str  # 设备 ID

class HandshakePackage(ClientPackage):
    action: Literal['handshake'] = 'handshake'
    data: HandshakeData

class TestPackage(ClientPackage):
    action: Literal['debug/test'] = 'debug/test'

class Send2PrivateData(BaseModel):
    bot_id: str

class Send2PrivatePackage(ClientPackage):
    action: Literal['send/private'] = 'send/private'
    data: Send2PrivateData

class GetBotsPackage(ClientPackage):
    action: Literal['bot/all'] = 'bot/all'

ClientPackageTypes: TypeAlias = Union[HandshakePackage, TestPackage, Send2PrivatePackage, GetBotsPackage]
