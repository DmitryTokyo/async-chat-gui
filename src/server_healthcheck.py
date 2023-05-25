from argparse import Namespace
import socket

from src.chat_connection import ChatConnection

from loguru import logger


async def check_server_health(chat_config: Namespace):
    expected_response = b'Welcome to chat! Post your message below. End it with an empty line.\n'
    try:
        async with ChatConnection(
            chat_config.host, chat_config.port_in, chat_config.user_hash, chat_config.save_info
        ) as (reader, writer):
            writer.write(''.encode())
            writer.write('\n\n'.encode())
            await writer.drain()
            message = await reader.readline()
            return message == expected_response
    except socket.gaierror:
        logger.exception('Error')
