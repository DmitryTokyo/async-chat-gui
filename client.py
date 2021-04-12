import asyncio
import logging
import json
from config import get_config

logger = logging.getLogger('server')
logging.basicConfig(level=logging.DEBUG)


async def submit_message(host, port, user_hash, user_conf):
    reader, writer = await asyncio.open_connection(host, port)
    authorisation = await authorise(reader, writer, user_hash, user_conf)
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


async def authorise(reader, writer, user_hash, user_conf):
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
    if user_conf:
        save_user_config(response)

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
    save_user_config(response)

    writer.close()
    await writer.wait_closed()
    return user_info['account_hash']


def save_user_config(response):
    user_info = json.loads(response.decode())

    with open('user.conf', 'w') as file:
        file.write(f'user_hash={user_info["account_hash"]}\n')
        file.write(f'nickname={user_info["nickname"]}\n')


async def main(config):
    user_hash = config.user_hash
    if not user_hash:
        user_hash = await register(config.host, config.port_in)
        config.user_conf = False
        
    if user_hash:
        await submit_message(config.host, config.port_in, user_hash, config.user_conf)


if __name__ == '__main__':
    config = get_config()
    asyncio.run(main(config))