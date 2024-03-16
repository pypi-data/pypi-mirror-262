from pydantic import BaseModel

class ScopedConfig(BaseModel):
    handshake_timeout: float = 30

class Config(BaseModel):
    wsshd: ScopedConfig = ScopedConfig()
