import asyncio
import logging
from config import get_config

logger_sender = logging.getLogger('sender')
logger_client = logging.getLogger('client')
logging.basicConfig(level=logging.DEBUG)


async def write_to_chat(host, port, user_hash):
    reader, writer = await asyncio.open_connection(host, port)
    response = await reader.readline()
    logger_sender.debug(response.decode())
    logger_client.debug(user_hash)
    send_message(writer, user_hash)
    response = await reader.readline()
    logger_sender.debug(response.decode())

    while True:
        message = input('Your message: ')
        send_message(writer, message)


def send_message(writer, message):
    writer.write(message.encode())
    writer.write('\n\n'.encode())


async def main(config):
    await write_to_chat(config.host, config.port_in, config.user_hash)


if __name__ == '__main__':
    config = get_config()
    asyncio.run(main(config))