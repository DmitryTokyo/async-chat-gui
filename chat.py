import asyncio
import aiofiles
from datetime import datetime
import configargparse


async def tcp_echo_client(host, port, path):
    while True:
        reader, writer = await asyncio.open_connection(host, port)

        data = await reader.readline()
        message_time = datetime.now().strftime('[%d.%m.%y %H:%M]')
        print(f'{message_time} {data.decode()}', end='')

        async with aiofiles.open(path, 'a') as file:
            await file.write(f'{message_time} {data.decode()}')


def get_config():
    parser = configargparse.ArgParser(default_config_files=['config.ini'])
    parser.add_argument('--host', type=str, help='host')
    parser.add_argument('--port', type=int, help='port')
    parser.add_argument('--path', type=str, help='chat file path')
    config, unknown = parser.parse_known_args()
    return config


def main():
    config = get_config()
    asyncio.run(tcp_echo_client(config.host, config.port, config.path))


if __name__ == '__main__':
    main()
