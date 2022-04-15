import asyncio
import socket

from autorization import authorize


class ChatConnection:

    def __init__(self, host, port, user_hash=None, used_data_file=None):
        self.sock = socket.create_connection((host, port))
        self.user_hash = user_hash
        self.user_data_file = used_data_file
        set_keepalive_linux(self.sock, 1, 1, 1)

    async def __aenter__(self):
        self.reader, self.writer = await asyncio.open_connection(sock=self.sock)
        if self.user_hash and self.user_data_file:
            await authorize(self.reader, self.writer, self.user_hash, self.user_data_file)
        return self.reader, self.writer

    async def __aexit__(self, *args):
        self.writer.close()
        await self.writer.wait_closed()


def set_keepalive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)