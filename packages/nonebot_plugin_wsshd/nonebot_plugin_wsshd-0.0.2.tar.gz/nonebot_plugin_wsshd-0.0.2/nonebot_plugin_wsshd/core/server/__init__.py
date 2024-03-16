import importlib
from pathlib import Path
from typing import Optional

from nonebot import get_app, logger
from nonebot.utils import path_to_module_name
from fastapi import FastAPI, APIRouter

import rsa

from . import store

def create_server():
    store.load_user_data()
    store.add_user(store.User(name='test', hashed_passwd='384fde3636e6e01e0194d2976d8f26410af3e846e573379cb1a09e2f0752d8cc'))

    if not store.PRIVATE_KEY_FILE.is_file() or not store.PUBLICK_KEY_FILE.is_file():
        pub, pri = rsa.newkeys(2048)
        public_key = pub.save_pkcs1()
        private_key = pri.save_pkcs1()

        store.PUBLICK_KEY_FILE.write_bytes(public_key)
        store.PRIVATE_KEY_FILE.write_bytes(private_key)

        store.PUBLICK_KEY = store.PUBLICK_KEY_FILE.read_bytes() if store.PUBLICK_KEY_FILE.is_file() else None
        store.PRIVATE_KEY = store.PRIVATE_KEY_FILE.read_bytes() if store.PRIVATE_KEY_FILE.is_file() else None

    app: FastAPI = get_app()

    root_apirouter = APIRouter(prefix='/wsshd', tags=['wsshd'])
    # 动态引入 core/server 下所有文件并添加 router
    for file in Path(__file__).parent.iterdir():
        if not file.is_file():
            continue

        if file.suffix.lower() != '.py':
            continue
        
        if file == Path(__file__):
            continue

        api_module = importlib.import_module(path_to_module_name(file))
        router_name: str = (
            'router'
            if not hasattr(api_module, '__fastapi_entry__') or not issubclass(type(api_module.__fastapi_entry__), str) else
            api_module.__fastapi_entry__
        )

        api_router: Optional[APIRouter] = getattr(api_module, router_name, None)
        if not isinstance(api_router, APIRouter):
            continue

        root_apirouter.include_router(api_router)

    app.include_router(root_apirouter)

    return app
