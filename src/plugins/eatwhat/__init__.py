#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eat What plugin - Help you decide what to eat
"""

import random
from datetime import datetime
from typing import Optional

from nonebot import get_driver, on_regex, on_message, get_bot
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.event import MessageEvent
from nonebot.adapters.telegram.message import Message
from nonebot.params import RegexStr
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule
from nonebot_plugin_apscheduler import scheduler

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
group_whitelist: set[str] = set()
user_whitelist: set[str] = set()
schedule_times: list[str] = []
random_probability: float = 0.0

# Get group whitelist
if hasattr(config, "eatwhat_group_whitelist"):
    group_whitelist = set(config.eatwhat_group_whitelist)

# Get user whitelist  
if hasattr(config, "eatwhat_user_whitelist"):
    user_whitelist = set(config.eatwhat_user_whitelist)

# Get schedule times
if hasattr(config, "eatwhat_schedule_times"):
    schedule_times = list(config.eatwhat_schedule_times)

# Get random probability
if hasattr(config, "eatwhat_random_probability"):
    random_probability = float(config.eatwhat_random_probability)


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


async def group_whitelist_check(bot: Bot, event: MessageEvent) -> bool:
    """Check if the message is from whitelisted group only"""
    chat_id = str(event.chat.id)
    return chat_id in group_whitelist


# Create matcher with regex and whitelist rule
csm = on_regex(
    r"吃(什么|啥)",
    rule=Rule(whitelist_check),
    priority=5,
    block=True
)

# Create matcher for random trigger (only in whitelisted groups, not blocked)
random_trigger = on_message(
    rule=Rule(group_whitelist_check),
    priority=10,
    block=False
)


@csm.handle()
async def handle_eatwhat(regex_str: str = RegexStr()):
    """Handle eatwhat command"""
    await csm.finish(f"是啊{regex_str}")


@random_trigger.handle()
async def handle_random_trigger(bot: Bot, event: MessageEvent):
    """Randomly trigger '吃什么' based on probability"""
    # Skip if the message itself is "吃什么" or "吃啥" (already handled by regex)
    message_text = event.message.extract_plain_text()
    if "吃什么" in message_text or "吃啥" in message_text:
        return
    
    # Random check
    if random.random() < random_probability:
        # Send "吃什么" to the group
        chat_id = event.chat.id
        await bot.send_message(chat_id=chat_id, text="吃什么")


# Schedule daily "吃什么" messages
async def send_scheduled_eatwhat():
    """Send '吃什么' to all whitelisted groups"""
    try:
        bot: Bot = get_bot()
    except ValueError:
        # No bot available
        return
    
    for chat_id_str in group_whitelist:
        try:
            chat_id = int(chat_id_str)
            await bot.send_message(chat_id=chat_id, text="吃什么")
        except Exception as e:
            # Log error but continue with other groups
            import logging
            logging.error(f"Failed to send scheduled message to {chat_id_str}: {e}")


# Add scheduled jobs for each time
for time_str in schedule_times:
    try:
        hour, minute = map(int, time_str.split(":"))
        scheduler.add_job(
            send_scheduled_eatwhat,
            "cron",
            hour=hour,
            minute=minute,
            id=f"eatwhat_schedule_{time_str.replace(':', '_')}",
            replace_existing=True,
        )
    except ValueError:
        # Invalid time format, skip
        import logging
        logging.warning(f"Invalid schedule time format: {time_str}, expected HH:MM")