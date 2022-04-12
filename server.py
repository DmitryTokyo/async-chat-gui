import asyncio
import aiofiles
from datetime import datetime
import logging
import socket
from contextlib import asynccontextmanager

from config import get_server_config

logger = logging.getLogger(__file__)


def set_keepalive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)


@asynccontextmanager
async def get_reader(sock):
    try:
        reader, writer = await asyncio.open_connection(sock=sock)
        yield reader
    finally:
        writer.close()
        await writer.wait_closed()


async def read_chat(host, port, path):
    while True:
        try:
            sock = socket.create_connection((host, port))
            set_keepalive_linux(sock, 1, 1, 1)
            async with get_reader(sock) as reader:
                while True:
                    data = await reader.readline()
                    message_time = datetime.now().strftime('[%d.%m.%y %H:%M]')
                    print(f'{message_time} {data.decode()}', end='')
                    async with aiofiles.open(path, 'a') as file:
                        await file.write(f'{message_time} {data.decode()}')

        except TimeoutError:
            logging.exception()
        except socket.gaierror:
            logging.exception()


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