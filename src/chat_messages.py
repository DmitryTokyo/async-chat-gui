from argparse import Namespace
from asyncio import Queue
import aiofiles
from datetime import datetime
import socket
from pathlib import Path

from chat_connection import ChatConnection

from loguru import logger


async def read_msgs_from(queue: Queue, server_config: Namespace) -> None:
    while True:
        try:
            async with ChatConnection(server_config.host, server_config.port_out) as (reader, writer):
                message = await reader.readline()
                message_time = datetime.now().strftime('[%d.%m.%y %H:%M]')
                queue.put_nowait(f'{message_time} {message.decode()}')
                await save_messages(
                    message_time=message_time,
                    message=message,
                    server_config=server_config,
                )

        except socket.gaierror as e:
            logger.exception(e)


async def save_messages(message_time: str, message: bytes, server_config: Namespace) -> None:
    async with aiofiles.open(server_config.path, 'a') as file:
        await file.write(f'{message_time} {message.decode()}')


async def load_messages_history_to(queue: Queue, server_config: Namespace) -> None:
    if not server_config.path:
        return

    chat_history_path = Path(server_config.path)
    if not chat_history_path.exists():
        logger.bind(
            module='server',
            file_path=str(chat_history_path),
        ).error('Wrong chat history file path')
        return

    with open(chat_history_path, 'r') as chat_history:
        for message in chat_history:
            queue.put_nowait(message)
