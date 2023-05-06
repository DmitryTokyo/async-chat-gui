from argparse import Namespace
from asyncio import Queue
import aiofiles
from datetime import datetime
import socket
from pathlib import Path

from chat_connection import ChatConnection

from loguru import logger

from src.utils.custom_error import InvalidToken


async def read_msgs_from(queue: Queue, chat_config: Namespace) -> None:
    while True:
        try:
            async with ChatConnection(chat_config.host, chat_config.port_out) as (reader, writer):
                message = await reader.readline()
                message_time = datetime.now().strftime('[%d.%m.%y %H:%M]')
                queue.put_nowait(f'{message_time} {message.decode()}')
                await save_messages(
                    message_time=message_time,
                    message=message,
                    chat_config=chat_config,
                )

        except socket.gaierror as e:
            logger.exception(e)


async def save_messages(message_time: str, message: bytes, chat_config: Namespace) -> None:
    async with aiofiles.open(chat_config.history_path, 'a') as file:
        await file.write(f'{message_time} {message.decode()}')


async def load_messages_history_to(messages_queue: Queue, chat_config: Namespace) -> None:
    if not chat_config.history_path:
        return

    chat_history_path = Path(chat_config.history_path)
    if not chat_history_path.exists():
        logger.bind(
            module='server',
            file_path=str(chat_history_path),
        ).error('Wrong chat history file path')
        return

    with open(chat_history_path, 'r') as chat_history:
        for message in chat_history:
            messages_queue.put_nowait(message)


async def send_msgs(sending_queue: Queue, exception_queue: Queue, chat_config: Namespace):
    try:
        async with ChatConnection(
            chat_config.host, chat_config.port_in, chat_config.user_hash, chat_config.save_info
        ) as (reader, writer):
            while True:
                msg = await sending_queue.get()
                if msg:
                    writer.write(msg.encode())
                    writer.write('\n\n'.encode())
                    await writer.drain()

    except socket.gaierror as e:
        logger.exception(e)
    except InvalidToken:
        print(f'User hash: {chat_config.user_hash} is unknown. Please check or get a new one.')
        exception_queue.put_nowait('Check your token. Server has not recognize it')
