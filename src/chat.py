import asyncio
from argparse import Namespace

from src.service import gui
from src.config import get_server_config
from src.chat_messages import read_msgs_from, load_messages_history_to


async def run_chat(server_config: Namespace):
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    await load_messages_history_to(messages_queue, server_config),
    await asyncio.gather(
        gui.draw(messages_queue, sending_queue, status_updates_queue),
        read_msgs_from(messages_queue, server_config),
    )


async def main():
    server_config = get_server_config()
    if server_config:
        await run_chat(server_config)

if __name__ in '__main__':
    asyncio.run(main())
