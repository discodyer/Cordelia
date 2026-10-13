#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cordelia - A Telegram bot based on NoneBot2
"""

import nonebot
from nonebot.adapters.telegram import Adapter as TelegramAdapter
from nonebot.adapters.telegram.config import AdapterConfig

# Initialize NoneBot
nonebot.init()
app = nonebot.get_asgi()

# Verify the configuration NoneBot actually loaded, rather than just the
# presence of the token in the process environment.
driver = nonebot.get_driver()
telegram_config = AdapterConfig(**driver.config.model_dump())
if not telegram_config.telegram_bots:
    raise RuntimeError(
        "No Telegram bots configured. Set telegram_bots in .env; "
        "Docker deployments must mount this file at /app/.env."
    )
nonebot.logger.info(
    f"Configured Telegram bots: {len(telegram_config.telegram_bots)}"
)
driver.register_adapter(TelegramAdapter)

# Load plugins
nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
