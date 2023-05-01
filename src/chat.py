import asyncio
from argparse import Namespace

from src.service import gui
from src.config import get_chat_config
from src.chat_messages import read_msgs_from, load_messages_history_to, send_msgs


async def run_chat(chat_config: Namespace):
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    await load_messages_history_to(messages_queue, chat_config),
    await asyncio.gather(
        gui.draw(messages_queue, sending_queue, status_updates_queue),
        read_msgs_from(messages_queue, chat_config),
        send_msgs(sending_queue, chat_config)
    )


async def main():
    chat_config = get_chat_config()
    if chat_config.host and chat_config.port_out and chat_config.port_in:
        await run_chat(chat_config)

if __name__ in '__main__':
    asyncio.run(main())
