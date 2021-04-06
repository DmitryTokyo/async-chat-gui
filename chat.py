import asyncio


async def tcp_echo_client():
    while True:
        reader, writer = await asyncio.open_connection(
            'minechat.dvmn.org', 5000)

        data = await reader.readline()
        print(data.decode(), end="")

asyncio.run(tcp_echo_client())
