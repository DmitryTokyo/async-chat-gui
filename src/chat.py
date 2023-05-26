import asyncio
import socket
from argparse import Namespace
from anyio import create_task_group, run
from tenacity import retry, stop_after_attempt, retry_if_exception_type
from src.service import gui
from src.config.chat_config import get_chat_config
from src.chat_messages import read_msgs_from, load_messages_history_to, send_msgs
from src.custom_error import InvalidToken, MaxRetriesExceededError, TkAppClosed
from loguru import logger

from src.utils.watchdog_messages import generate_watchdog_logger_messages


@retry(
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(socket.gaierror)
)
async def handle_connection(chat_config: Namespace) -> None:
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    exception_queue = asyncio.Queue()
    watchdog_queue = asyncio.Queue()
    await load_messages_history_to(messages_queue, watchdog_queue, chat_config)
    async with create_task_group() as tg:
        tg.start_soon(gui.draw, messages_queue, sending_queue, status_updates_queue, exception_queue)
        tg.start_soon(read_msgs_from, messages_queue, status_updates_queue, watchdog_queue, chat_config)
        tg.start_soon(send_msgs, sending_queue, exception_queue, status_updates_queue, watchdog_queue, chat_config)
        tg.start_soon(watch_for_connection, watchdog_queue)

    raise MaxRetriesExceededError


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

    logger.bind(
        module='main',
        action='tasks_cancellation',
    ).info('All task was canceled')


async def main():
    chat_config = get_chat_config()
    if chat_config.host and chat_config.port_out and chat_config.port_in:
        try:
            await handle_connection(chat_config=chat_config)
        except (MaxRetriesExceededError, InvalidToken, TkAppClosed):
            cancel_all_tasks()

if __name__ in '__main__':
    run(main)
