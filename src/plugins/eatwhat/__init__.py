#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eat What plugin - Help you decide what to eat
"""

from nonebot import on_keyword
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.event import MessageEvent
from nonebot.plugin import PluginMetadata
# from nonebot.rule import to_me

__plugin_meta__ = PluginMetadata(
    name="echo",
    description="吃什么",
    usage="吃什么",
    type="application",
    config=None,
    supported_adapters=None,
)

csm = on_keyword("吃什么", priority=5, block=True)


@csm.handle()
async def handle_ping(bot: Bot, event: MessageEvent):
    await csm.finish("吃什么")

