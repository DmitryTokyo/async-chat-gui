import asyncio
import logging
import json
import socket

from chat_connection import set_keepalive_linux, ChatConnection
from config import get_client_config, update_user_config
from custom_error import HashError

logger = logging.getLogger('server ')


async def submit_message(host, port, user_hash, upd_user_file):
    while True:
        try:
            sock = socket.create_connection((host, port))
            set_keepalive_linux(sock, 1, 1, 1)
            async with ChatConnection(sock, user_hash, upd_user_file) as (reader, writer):
                while True:
                    try:
                        message = input('Your message: ')
                        if message == 'Exit!':
                            return
                        writer.write(message.encode())
                        writer.write('\n\n'.encode())
                        await writer.drain()
                    except socket.error:
                        break
        except TimeoutError as e:
            logging.exception(e)
        except socket.gaierror as e:
            logging.exception(e)
        except HashError:
            print('Please check your hash or get a new one')
            break


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

    nicname = input()
    writer.write(nicname.encode())
    writer.write('\n'.encode())

    response = await reader.readline()
    logger.debug(response.decode())
    user_info = json.loads(response.decode())
    update_user_config(response)

    writer.close()
    await writer.wait_closed()
    return user_info['account_hash']


async def main():
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    config = get_client_config()
    user_hash = config.user_hash
    if not user_hash:
        user_hash = await register(config.host, config.port_in)
        config.user_conf = False
        
    if user_hash:
        await submit_message(config.host, config.port_in, user_hash, config.upd_user_file)


if __name__ == '__main__':
    asyncio.run(main())