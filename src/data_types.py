from enum import Enum


class ReadConnectionStateChanged(Enum):
    INITIATED = 'connecting...'
    ESTABLISHED = 'connection established'
    CLOSED = 'connection terminated'


class SendingConnectionStateChanged(Enum):
    INITIATED = 'connecting...'
    ESTABLISHED = 'connection established'
    CLOSED = 'connection terminated'


class NicknameReceived:
    def __init__(self, nickname):
        self.nickname = nickname
