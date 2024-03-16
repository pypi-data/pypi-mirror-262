from typing import Dict

from ...events import bot
from .client_types import ActionTypes, PackageCallbackType

callbacks: Dict[ActionTypes, PackageCallbackType] = {
    'bot/all': bot.get_all_bots
}