import asyncio
from config import get_config


async def write_to_chat(host, port, user_hash):
    reader, writer = await asyncio.open_connection(host, port)
    await reader.readline()
    send_message(writer, user_hash)
    await reader.readline()

    while True:
        message = input('Type smth: ')
        send_message(writer, message)


def send_message(writer, message):
    writer.write(message.encode())
    writer.write('\n\n'.encode())


async def main(config):
    await write_to_chat(config.host, config.port_in, config.user_hash)


if __name__ == '__main__':
    config = get_config()
    asyncio.run(main(config))