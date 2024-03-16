from pydantic import BaseModel
from json import load
from typing import Literal, Dict
from typing_extensions import TypeAlias

import nonebot_plugin_localstore as store

USER_DATA_FILE = store.get_data_file('wsshd', 'users.json')
PUBLICK_KEY_FILE = store.get_data_file('wsshd', 'public.key')
PRIVATE_KEY_FILE = store.get_data_file('wsshd', 'private.key')

PUBLICK_KEY = PUBLICK_KEY_FILE.read_bytes() if PUBLICK_KEY_FILE.is_file() else None
PRIVATE_KEY = PRIVATE_KEY_FILE.read_bytes() if PRIVATE_KEY_FILE.is_file() else None

HashMethodTypes: TypeAlias = Literal['sha512', 'sha256', 'md5']
class User(BaseModel):
    name: str
    hashed_passwd: str
    hash_method: HashMethodTypes = 'sha256'
    allow_login: int = False

class UserData(BaseModel):
    users: Dict[str, User] = {}

USER_DATA: UserData = UserData()

def save_user_data():
    USER_DATA_FILE.write_text(USER_DATA.model_dump_json())

def load_user_data():
    if USER_DATA_FILE.is_file():
        with USER_DATA_FILE.open('r', encoding='u8') as fp:
            loaded = load(fp)
            for username, content in loaded['users'].items():
                USER_DATA.users[username] = User(**content)
    else:
        save_user_data()

def add_user(user: User):
    USER_DATA.users[user.name] = user
    save_user_data()

def remove_user(name: str):
    USER_DATA.users.pop(name, None)
    save_user_data()
