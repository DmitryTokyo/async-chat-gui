import asyncio
from config import get_config
from access import access_to_chat, get_user_hash


async def write_to_chat(host, port, user_hash):
    reader, writer = await asyncio.open_connection(host, port)
    access = await access_to_chat(reader, writer, user_hash)
    if access:
        while True:
            message = input('Your message: ')
            send_message(writer, message)


def send_message(writer, message):
    writer.write(message.encode())
    writer.write('\n\n'.encode())


async def main(config):
    if not config.user_hash:
        user_hash = await get_user_hash(config.host, config.port_in)
        
    await write_to_chat(config.host, config.port_in, config.user_hash)
    

if __name__ == '__main__':
    config = get_config()
    asyncio.run(main(config))