import logging
import json
import asyncio

logger_sender = logging.getLogger('sender')
logger_client = logging.getLogger('client')
logging.basicConfig(level=logging.DEBUG)


async def access_to_chat(reader, writer, user_hash):
    response = await reader.readline()
    logger_sender.debug(response.decode())
    logger_client.debug(user_hash)

    writer.write(user_hash.encode())
    writer.write('\n\n'.encode())
    
    response = await reader.readline()
    logger_sender.debug(response.decode())

    if not json.loads(response.decode()):
        logger_sender.error('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        return False
    return True


async def get_user_hash(host, port):
    print('''Для доступа к чату нужен user hash. Если у вас он есть,
    укажите его при запуске скрипта. Если нет, получите новый user hash.''')

    response = input('Вам нужен новый user_hash (y/n)? ')
    if response == 'y':
        reader, writer = await asyncio.open_connection(host, port)

        response = await reader.readline()
        logger_sender.debug(response.decode())
        writer.write('\n'.encode())
        response = await reader.readline()
        logger_sender.debug(response.decode())
        nicname = input()
        writer.write(nicname.encode())
        writer.write('\n'.encode())
        response = await reader.readline()
        logger_sender.debug(response.decode())
        user_info = json.loads(response.decode())
        
        with open('config.ini', 'a') as file:
            file.write(f'\nuser_hash={user_info["account_hash"]}')
        
        writer.close()
        await writer.wait_closed()
    return user_info('account_hash')
    