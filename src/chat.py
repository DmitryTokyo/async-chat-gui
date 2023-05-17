import asyncio
import time
from argparse import Namespace

from src.service import gui
from src.config.chat_config import get_chat_config
from src.chat_messages import read_msgs_from, load_messages_history_to, send_msgs
from src.custom_error import InvalidToken
from loguru import logger

from src.utils.watchdog_messages import generate_watchdog_logger_messages


async def run_chat(chat_config: Namespace):
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    exception_queue = asyncio.Queue()
    watchdog_queue = asyncio.Queue()
    await load_messages_history_to(messages_queue, watchdog_queue, chat_config),
    try:
        await asyncio.gather(
            gui.draw(messages_queue, sending_queue, status_updates_queue, exception_queue),
            read_msgs_from(messages_queue, status_updates_queue, watchdog_queue, chat_config),
            send_msgs(sending_queue, exception_queue, status_updates_queue, watchdog_queue, chat_config),
            watch_for_connection(watchdog_queue)
        )
    except InvalidToken:
        cancel_all_tasks()


async def watch_for_connection(watchdog_queue: asyncio.Queue) -> None:
    while True:
        msg = await watchdog_queue.get()
        if msg:
            logger_messages = generate_watchdog_logger_messages(watchdog_message=msg)
            logger.bind(
                module='main',
                action='watchdog_logger',
            ).debug(logger_messages)


def cancel_all_tasks():
    tasks = asyncio.all_tasks()
    current = asyncio.current_task()
    tasks.remove(current)
    for task in tasks:
        task.cancel()


async def main():
    chat_config = get_chat_config()
    if chat_config.host and chat_config.port_out and chat_config.port_in:
        await run_chat(chat_config)

if __name__ in '__main__':
    asyncio.run(main())
