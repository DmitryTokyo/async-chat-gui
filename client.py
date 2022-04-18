import asyncio
import logging
import socket

from chat_connection import ChatConnection
from config import get_client_config
from custom_error import HashError
from registration import register

logger = logging.getLogger('server')


async def submit_message(host, port, user_hash, upd_user_file):
    try:
        async with ChatConnection(host, port, user_hash, upd_user_file) as (reader, writer):
            while True:
                message = input('Your message (Type Exit! for chat exit): ')
                if message == 'Exit!':
                    return
                writer.write(message.encode())
                writer.write('\n\n'.encode())
                await writer.drain()

    except socket.gaierror as e:
        logging.exception(e)
    except HashError:
        print(f'User hash: {user_hash} is unknown. Please check or get a new one.')


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