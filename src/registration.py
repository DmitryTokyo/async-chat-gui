import asyncio
import json
import logging

from src.config import save_user_info

logger = logging.getLogger('server')


async def register(host, port):
    print('''To access the chat you need the user hash. Please pass it as 
    argument --user_hash or get a new one ''')

    response = input('Do you need a new user hash (y/n)? ')
    if response == 'n':
        return None

    reader, writer = await asyncio.open_connection(host, port)

    response = await reader.readline()
    logger.debug(response.decode())
    writer.write('\n'.encode())
    response = await reader.readline()
    logger.debug(response.decode())

    nickname = input('Input your nickname: ')
    writer.write(nickname.encode())
    writer.write('\n'.encode())

    response = await reader.readline()
    logger.debug(response.decode())
    user_info = json.loads(response.decode())
    save_user_info(response)

    writer.close()
    await writer.wait_closed()
    return user_info['account_hash']