#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ping plugin - Reply pong to /ping command
"""

from nonebot import on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.event import MessageEvent
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="ping",
    description="Reply pong to /ping command",
    usage="/ping",
)

# Create a command handler for /ping
ping = on_command("ping", priority=5, block=True)


@ping.handle()
async def handle_ping(bot: Bot, event: MessageEvent):
    """Handle /ping command, reply with pong"""
    await ping.finish("pong")
