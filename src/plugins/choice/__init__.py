"""从用户提供的选项中随机选择一个。"""

import random

from nonebot import on_command, on_startswith
from nonebot.adapters import Message
from nonebot.adapters.telegram.event import MessageEvent
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="choice",
    description="从空格分隔的选项中随机选择一个",
    usage="/choice 选项1 选项2 或 帮我选 选项1 选项2",
    type="application",
    config=None,
    supported_adapters={"nonebot.adapters.telegram"},
)

choice = on_command("choice", force_whitespace=True, priority=5, block=True)
help_choose = on_startswith("帮我选", priority=5, block=True)


def choose_reply(text: str) -> str:
    options = text.split()
    if not options:
        return "请提供选项，例如：/choice 苹果 香蕉"
    return f"我选: {random.choice(options)}"


@choice.handle()
async def handle_choice(message: Message = CommandArg()):
    await choice.finish(choose_reply(message.extract_plain_text()))


@help_choose.handle()
async def handle_help_choose(event: MessageEvent):
    options_text = event.get_plaintext()[len("帮我选"):]
    await help_choose.finish(choose_reply(options_text))
