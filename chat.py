import asyncio
import aiofiles
from datetime import datetime


async def tcp_echo_client():
    while True:
        reader, writer = await asyncio.open_connection(
            'minechat.dvmn.org', 5000)

        data = await reader.readline()
        message_time = datetime.now().strftime('[%d.%m.%y %H:%M]')
        print(f'{message_time} {data.decode()}', end='')

        async with aiofiles.open('tmp.txt', 'a') as file:
            await file.write(f'{message_time} {data.decode()}')

asyncio.run(tcp_echo_client())
