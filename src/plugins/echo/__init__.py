#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo plugin - Repeat what you said to /echo [text] command
"""

from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
# from nonebot.rule import to_me

__plugin_meta__ = PluginMetadata(
    name="echo",
    description="Repeat what you said",
    usage="/echo [text]",
    type="application",
    config=None,
    supported_adapters=None,
)

echo = on_command("echo", priority=5, block=True)


@echo.handle()
async def handle_echo(message: Message = CommandArg()):
    if any((not seg.is_text()) or str(seg) for seg in message):
        await echo.send(message=message)

