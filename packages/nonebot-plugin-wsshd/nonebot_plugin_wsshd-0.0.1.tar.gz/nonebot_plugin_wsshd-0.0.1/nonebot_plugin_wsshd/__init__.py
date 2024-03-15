from nonebot import get_plugin_config, get_driver
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="wsshd",
    description="",
    usage="",
    config=Config,
)


driver = get_driver()
global_config = driver.config
config = get_plugin_config(Config)

from .core.server import app
