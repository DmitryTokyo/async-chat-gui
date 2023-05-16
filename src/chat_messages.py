import asyncio
from argparse import Namespace
from asyncio import Queue
import aiofiles
from datetime import datetime
import socket
from pathlib import Path

from chat_connection import ChatConnection

from loguru import logger

from src.data_types import ReadConnectionStateChanged, SendingConnectionStateChanged, NicknameReceived, WatchDogMessage
from src.custom_error import InvalidToken
from src.config import settings


async def read_msgs_from(
    messages_queue: Queue,
    status_updates_queue: Queue,
    watchdog_queue: Queue,
    chat_config: Namespace,
) -> None:
    retry_count = 0
    while True:
        try:
            async with ChatConnection(chat_config.host, chat_config.port_out) as (reader, writer):
                message = await reader.readline()
                message_time = datetime.now().strftime('[%d.%m.%y %H:%M]')
                messages_queue.put_nowait(f'{message_time} {message.decode()}')
                await save_messages(
                    message_time=message_time,
                    message=message,
                    chat_config=chat_config,
                )
                status_updates_queue.put_nowait(ReadConnectionStateChanged.ESTABLISHED)
                watchdog_queue.put_nowait(WatchDogMessage.NEW_CHAT_MESSAGE)
        except (socket.gaierror, TimeoutError) as e:
            if retry_count >= settings.MAX_CONNECTION_ATTEMPT_RETRY:
                logger.bind(
                    module='server',
                    action='reading',
                    error=str(e),
                ).error('Connection lost. Exceeded maximum connection retries.')
                raise socket.gaierror
            retry_count += 1
            status_updates_queue.put_nowait(ReadConnectionStateChanged.INITIATED)
            logger.bind(
                module='server',
                action='reading',
                error=str(e)
            ).warning(f'Connection lost. Retrying ({retry_count}/{settings.MAX_CONNECTION_ATTEMPT_RETRY})....')
            await asyncio.sleep(settings.CONNECTION_RETRY_TIMEOUT)


async def save_messages(message_time: str, message: bytes, chat_config: Namespace) -> None:
    async with aiofiles.open(chat_config.history_path, 'a') as file:
        await file.write(f'{message_time} {message.decode()}')


async def load_messages_history_to(messages_queue: Queue, watchdog_queue: Queue, chat_config: Namespace) -> None:
    if not chat_config.history_path:
        return

    chat_history_path = Path(chat_config.history_path)
    if not chat_history_path.exists():
        logger.bind(
            module='server',
            action='load chat history',
            file_path=str(chat_history_path),
        ).error('Wrong chat history file path')
        return

    with open(chat_history_path, 'r') as chat_history:
        for message in chat_history:
            messages_queue.put_nowait(message)

    watchdog_queue.put_nowait(WatchDogMessage.LOADED_CHAT_HISTORY)


async def send_msgs(
    sending_queue: Queue,
    exception_queue: Queue,
    status_updates_queue: Queue,
    watchdog_queue: Queue,
    chat_config: Namespace,
) -> None:
    retry_count = 0
    watchdog_queue.put_nowait(WatchDogMessage.BEFORE_AUTH)
    try:
        async with ChatConnection(
            chat_config.host, chat_config.port_in, chat_config.user_hash, chat_config.save_info
        ) as (reader, writer):
            status_updates_queue.put_nowait(SendingConnectionStateChanged.ESTABLISHED)
            status_updates_queue.put_nowait(NicknameReceived(chat_config.nickname))
            watchdog_queue.put_nowait(WatchDogMessage.AUTH_DONE)
            while True:
                msg = await sending_queue.get()
                if msg:
                    writer.write(msg.encode())
                    writer.write('\n\n'.encode())
                    await writer.drain()
                    watchdog_queue.put_nowait(WatchDogMessage.SENT_MESSAGE)

    except (socket.gaierror, TimeoutError) as e:
        if retry_count >= settings.MAX_CONNECTION_ATTEMPT_RETRY:
            logger.bind(
                module='client',
                action='sending',
                error=str(e)
            ).error('Connection lost. Exceeded maximum connection retries.')
            raise socket.gaierror
        retry_count += 1
        status_updates_queue.put_nowait(SendingConnectionStateChanged.INITIATED)
        logger.bind(
            module='client',
            action='sending',
            error=str(e),
        ).warning(f'Connection lost. Retrying ({retry_count}/{settings.MAX_CONNECTION_ATTEMPT_RETRY})....')
        await asyncio.sleep(settings.CONNECTION_RETRY_TIMEOUT)
    except InvalidToken:
        print(f'User hash: {chat_config.user_hash} is unknown. Please check or get a new one.')
        exception_queue.put_nowait('Check your token. Server has not recognize it')
