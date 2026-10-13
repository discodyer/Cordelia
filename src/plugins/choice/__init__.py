"""从用户提供的选项中随机选择一个。"""

import os
import random
import re
from re import Match

from nonebot import get_driver, on_regex, on_startswith
from nonebot.adapters import Bot, Event
from nonebot.adapters.telegram.event import MessageEvent
from nonebot.adapters.telegram.model import ReplyParameters
from nonebot.params import RegexMatched
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule

__plugin_meta__ = PluginMetadata(
    name="choice",
    description="从空格分隔的选项中随机选择一个",
    usage="/choice 选项1 选项2 或 帮我选 选项1 选项2",
    type="application",
    config=None,
    supported_adapters={"nonebot.adapters.telegram"},
)

CHOICE_PATTERN = r"^/choice(?:@(?P<bot>[A-Za-z0-9_]+))?(?:[ \t]+(?P<args>.*))?$"

# Telegram represents `/choice@BotName` as a bot command. Match the optional
# target explicitly so that this bot only responds to its own username.
async def _choice_target(
    bot: Bot,
    event: Event,
) -> bool:
    matched = re.fullmatch(CHOICE_PATTERN, event.get_plaintext())
    if matched is None:
        return False
    target = matched.group("bot")
    username = (
        bot.username
        or getattr(get_driver().config, "telegram_bot_username", None)
        or os.getenv("TELEGRAM_BOT_USERNAME")
    )
    return not target or (
        username is not None and target.casefold() == username.casefold()
    )


choice = on_regex(
    CHOICE_PATTERN,
    rule=Rule(_choice_target),
    priority=5,
    block=True,
)
help_choose = on_startswith("帮我选", priority=5, block=True)


def choose_reply(text: str) -> str:
    options = text.split()
    if not options:
        return "请提供选项，例如：/choice 苹果 香蕉"
    return f"我选: {random.choice(options)}"


@choice.handle()
async def handle_choice(
    event: MessageEvent,
    matched: Match[str] = RegexMatched(),
):
    await choice.finish(
        choose_reply(matched.group("args") or ""),
        reply_parameters=ReplyParameters(message_id=event.message_id),
    )


@help_choose.handle()
async def handle_help_choose(event: MessageEvent):
    options_text = event.get_plaintext()[len("帮我选"):]
    await help_choose.finish(
        choose_reply(options_text),
        reply_parameters=ReplyParameters(message_id=event.message_id),
    )
