from nonebot import get_plugin_config, get_driver, require
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="wsshd",
    description="",
    usage="",
    config=Config,
)

require('nonebot_plugin_localstore')

driver = get_driver()
global_config = driver.config
config = get_plugin_config(Config).wsshd

from .core.server import create_server
create_server()
