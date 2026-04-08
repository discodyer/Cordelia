#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cordelia - A Telegram bot based on NoneBot2
"""

import nonebot
from nonebot.adapters.telegram import Adapter as TelegramAdapter

# Initialize NoneBot
nonebot.init()
app = nonebot.get_asgi()

# Register adapters with polling config
driver = nonebot.get_driver()
driver.register_adapter(TelegramAdapter)

# Load plugins
nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
