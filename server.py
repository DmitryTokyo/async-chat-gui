import asyncio
import aiofiles
from datetime import datetime
import logging
import socket

from chat_connection import set_keepalive_linux, ChatConnection
from config import get_server_config

logger = logging.getLogger(__file__)


async def read_chat(host, port, path):
    while True:
        try:
            async with ChatConnection(host, port) as (reader, writer):
                while True:
                    data = await reader.readline()
                    message_time = datetime.now().strftime('[%d.%m.%y %H:%M]')
                    print(f'{message_time} {data.decode()}', end='')
                    async with aiofiles.open(path, 'a') as file:
                        await file.write(f'{message_time} {data.decode()}')

        except socket.gaierror as e:
            logging.exception(e)


async def main():
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    config = get_server_config()

    if config:
        await read_chat(config.host, config.port_out, config.path)


if __name__ == '__main__':
    asyncio.run(main())