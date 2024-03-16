from typing import Any, Mapping, Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.exceptions import WebSocketException
from starlette.background import BackgroundTask

class WSServerData(BaseModel):
    code: int = 1000
    msg: str = 'success'
    data: Any = None

class WSUnknownAction(WSServerData):
    code: int = 1003
    msg: str = 'unknown action'

class WSWrongPkgStruct(WSServerData):
    code: int = 1003
    msg: str = 'wrong package content struct'

class WSSendPublickKey(WSServerData):
    code: int = 1000
    msg: str = 'public key'
    data: str

class WSFailedGotRes(WSServerData):
    code: int = 1011
    msg: str = 'failed to get action result'

class WSUserLoginSuccessfully(WSServerData):
    msg: str = 'login success'

class WSSendPrivateUnknownBotId(WSServerData):
    code: int = 1003
    msg: str = 'unknown bot id'

class GetBots(WSServerData):
    pass


WRONG_CANNOT_HANDSHAKE = WSServerData(code=1003, msg='cannot handshake after connected')
WRONG_NOT_HANDSHAKE = WSServerData(code=1003, msg='you should send `handshake` package first of all')
WRONG_HANDSHAKE_TIMEOUT = WSServerData(code=1003, msg='handshake timeout')

class WSServerResponse(JSONResponse):
    def __init__(self, content: WSServerData, status_code: Optional[int] = None, headers: Optional[Mapping[str, str]] = None, background: Optional[BackgroundTask] = None):
        code = status_code if status_code is not None else content.code

        super().__init__(content.model_dump(), code, headers, 'application/json', background)

class WSServerEception(WebSocketException):
    def __init__(self, content: WSServerData, status_code: Optional[int] = None):
        code = status_code if status_code is not None else content.code

        super().__init__(code, content.model_dump_json())
