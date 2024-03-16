__fastapi_entry__ = 'ws'
from dataclasses import asdict
from pydantic_core import ValidationError
from nonebot import logger
from nonebot.exception import MatcherException

from fastapi import APIRouter, Depends, WebSocket

from asyncio.exceptions import TimeoutError
from async_timeout import timeout

from ast import literal_eval

import rsa
import hashlib

from ... import config
from .store import USER_DATA, User, PRIVATE_KEY, PUBLICK_KEY
from .client import Client, create_client
from .client_types import HandshakePackage, ClientPackage
from .shared import package_handler, send_pydantic_model, WSCloseException
from .server_types import WRONG_NOT_HANDSHAKE, WRONG_HANDSHAKE_TIMEOUT, WSWrongPkgStruct, WSSendPublickKey, WSServerData, WSUserLoginSuccessfully
from .callbacks import callbacks

ws = APIRouter(prefix='/ws', tags=['ws', 'websocket'],)

async def userChecker(pkg: HandshakePackage, ws: WebSocket):
    username, password = pkg.data.username, literal_eval(pkg.data.password)
    if not isinstance(password, bytes):
        raise WSCloseException(code=1003, msg='password must be python bytes string')

    user = USER_DATA.users.get(username, None)
    if not isinstance(user, User):
        raise WSCloseException(code=1003, msg='unknown user')

    if PRIVATE_KEY is None or PUBLICK_KEY is None:
        raise WSCloseException(code=1011, msg='failed to load `PRIVATE_KEY` and/or `PUBLICK_KEY`')

    try:
        private_key = rsa.PrivateKey.load_pkcs1(PRIVATE_KEY)
    except Exception as e:
        raise WSCloseException(code=1011, msg=f'failed to load `PRIVATE_KEY`: {repr(e)}')

    password = rsa.decrypt(password, private_key)
    hash_func = getattr(hashlib, user.hash_method, None)
    hashlib.sha256().hexdigest()
    if not callable(hash_func):
        raise WSCloseException(code=1011, msg=f'unknown hash method: {user.hash_method}')
    
    if hash_func(password).hexdigest() != user.hashed_passwd:
        raise WSCloseException(code=1003, msg='wrong username and/or password')
    
    await send_pydantic_model(ws, WSUserLoginSuccessfully())


async def client_handshake(ws: WebSocket) -> Client:
    pkg = await package_handler(ws)

    if not isinstance(pkg, HandshakePackage):
        if isinstance(pkg, ValidationError):
            await send_pydantic_model(ws, WSWrongPkgStruct(data=pkg.errors()))
            raise WSCloseException

        elif isinstance(pkg, ClientPackage):
            await send_pydantic_model(ws, WSWrongPkgStruct(data={'error': 'is not `handshake` package'}))
            raise WSCloseException

        else:
            await send_pydantic_model(ws, WRONG_NOT_HANDSHAKE)
            raise WSCloseException
    
    await userChecker(pkg, ws)

    try:
        client = create_client(pkg, ws, callbacks)
        return client
    except ValidationError as e:
        await send_pydantic_model(ws, WSWrongPkgStruct(data=e.errors()))
        raise WSCloseException

@ws.websocket('/')
async def ws_main(ws: WebSocket):
    if PUBLICK_KEY is None:
        await send_pydantic_model(ws, WSServerData(code=1011, msg='failed to load `PUBLIC_KEY`'))
        raise WSCloseException(code=1011, msg='failed to load `PUBLIC_KEY`')

    try:
        with timeout(config.handshake_timeout):
            await ws.accept()
            await send_pydantic_model(ws, (WSSendPublickKey(data=PUBLICK_KEY.decode())))
            client = await client_handshake(ws)
    except TimeoutError:
        await send_pydantic_model(ws, WRONG_HANDSHAKE_TIMEOUT)
        logger.debug('code: {}', WRONG_HANDSHAKE_TIMEOUT.code)
        await ws.close(WRONG_HANDSHAKE_TIMEOUT.code)
        return
    except WSCloseException as e:
        await send_pydantic_model(ws, WSServerData(code=e.code, msg=e.msg))
        await ws.close(e.code)
        return

    try:
        await client.mainloop()
    except WSCloseException as e:
        await ws.close(e.code)
        return
