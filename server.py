import asyncio
import aiofiles
from datetime import datetime
from config import get_config


async def read_chat(host, port, path):
    while True:
        reader, writer = await asyncio.open_connection(host, port)
        data = await reader.readline()
        message_time = datetime.now().strftime('[%d.%m.%y %H:%M]')
        print(f'{message_time} {data.decode()}', end='')

        async with aiofiles.open(path, 'a') as file:
            await file.write(f'{message_time} {data.decode()}')


async def main(config):
    await read_chat(config.host, config.port_out, config.path)


if __name__ == '__main__':
    config = get_config()
    asyncio.run(main(config))