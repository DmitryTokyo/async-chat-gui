import asyncio
import logging
import json
from config import get_config

logger = logging.getLogger('server')
logging.basicConfig(level=logging.DEBUG)


async def submit_message(host, port, user_hash):
    reader, writer = await asyncio.open_connection(host, port)
    authorisation = await authorise(reader, writer, user_hash)
    logger.info('For leaving chat type: Exit!')

    if authorisation:
        while True:
            message = input('Your message: ')
            if message == 'Exit!':
                writer.close()
                await writer.wait_closed()
                break

            writer.write(message.encode())
            writer.write('\n\n'.encode())


async def authorise(reader, writer, user_hash):
    response = await reader.readline()
    logger.debug(response.decode())

    writer.write(user_hash.encode())
    writer.write('\n\n'.encode())
    
    response = await reader.readline()
    logger.debug(response.decode())

    if not json.loads(response.decode()):
        logger.error(f'User hash: {user_hash}')
        logger.error('''Неизвестный токен. Проверьте его или
                               зарегистрируйте заново.''')
        return False

    return True


async def register(host, port):
    print('''Для доступа к чату нужен user hash. Если у вас он есть,
    укажите его при запуске скрипта. Если нет, получите новый user hash.''')

    response = input('Вам нужен новый user_hash (y/n)? ')
    if response == 'n':
        return None

    reader, writer = await asyncio.open_connection(host, port)

    response = await reader.readline()
    logger.debug(response.decode())
    writer.write('\n'.encode())
    response = await reader.readline()
    logger.debug(response.decode())

    nicname = input()
    writer.write(nicname.encode())
    writer.write('\n'.encode())

    response = await reader.readline()
    logger.debug(response.decode())
    user_info = json.loads(response.decode())

    with open('config.ini', 'a') as file:
        file.write(f'\nuser_hash={user_info["account_hash"]}')

    writer.close()
    await writer.wait_closed()
    return user_info['account_hash']


async def main(config):
    user_hash = config.user_hash
    if not user_hash:
        user_hash = await register(config.host, config.port_in)
    
    await submit_message(config.host, config.port_in, user_hash)


if __name__ == '__main__':
    config = get_config()
    asyncio.run(main(config))