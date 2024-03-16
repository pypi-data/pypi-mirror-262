from nonebot import get_bots, get_bot
from fastapi import WebSocket

from ..core.server import server_types, client_types
from ..core.server.server_types import WSServerData

async def send_private(ws: WebSocket, pkg: client_types.Send2PrivatePackage):
    try:
        bot = get_bot(pkg.data.bot_id)
    except KeyError:
        return server_types.WSSendPrivateUnknownBotId(data={'target': pkg.data.bot_id})

async def get_all_bots(ws: WebSocket, pkg: client_types.GetBotsPackage) -> server_types.GetBots:
    result = {}

    bots = get_bots()
    for bot_id, bot in bots.items():
        
        result[bot_id] = {
            'config': bot.config.model_dump_json(),
            'adapter': {
                'name': bot.adapter.get_name(),
            }
        }
    
    return server_types.GetBots(data=result)
