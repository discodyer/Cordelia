#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eat What plugin - Help you decide what to eat
"""

import re
from nonebot import get_driver, on_regex
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.event import MessageEvent
from nonebot.params import RegexStr
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule

__plugin_meta__ = PluginMetadata(
    name="吃什么",
    description="吃什么",
    usage="吃什么/吃啥",
    type="application",
    config=None,
    supported_adapters=None,
)

# Get whitelist configuration from environment
driver = get_driver()
config = driver.config

# Parse whitelist from config
group_whitelist = set()
user_whitelist = set()

# Get group whitelist
if hasattr(config, "eatwhat_group_whitelist"):
    group_whitelist = set(config.eatwhat_group_whitelist)

# Get user whitelist  
if hasattr(config, "eatwhat_user_whitelist"):
    user_whitelist = set(config.eatwhat_user_whitelist)


async def whitelist_check(bot: Bot, event: MessageEvent) -> bool:
    """Check if the message is from whitelisted group or user"""
    # Get chat_id from event
    chat_id = str(event.chat.id)
    
    # Get user_id from event (from_ is the attribute name, aliased from "from" in Telegram API)
    user_id = str(event.from_.id) if hasattr(event, 'from_') and event.from_ else None
    
    # Check if chat_id is in group whitelist (for group chats)
    if chat_id in group_whitelist:
        return True
    
    # Check if user_id is in user whitelist (for private chats or whitelisted users in groups)
    if user_id and user_id in user_whitelist:
        return True
    
    return False


# Create matcher with regex and whitelist rule
csm = on_regex(
    r"吃(什么|啥)",
    rule=Rule(whitelist_check),
    priority=5,
    block=True
)


@csm.handle()
async def handle_eatwhat(regex_str: str = RegexStr()):
    """Handle eatwhat command"""
    await csm.finish(f"是啊{regex_str}")