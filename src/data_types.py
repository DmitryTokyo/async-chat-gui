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


class WatchDogMessage(Enum):
    BEFORE_AUTH = 'Prompt before auth'
    AUTH_DONE = 'Authorization done'
    NEW_CHAT_MESSAGE = 'New message in chat'
    SENT_MESSAGE = 'Message sent'
    LOADED_CHAT_HISTORY = 'Chat history loaded'
