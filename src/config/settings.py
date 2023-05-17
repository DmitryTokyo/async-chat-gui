import os


CHAT_HISTORY_SAVE_PATH = os.getenv('CHAT_HISTORY_SAVE_PATH', default='./src/chat_history/chat.txt')

USER_CONFIGURATION_FILE_PATH = os.getenv('USER_CONFIGURATION_SAVE_PATH', default='./src/config/user.conf')

SERVER_CONFIGURATION_FILE_PATH = os.getenv('SERVER_CONFIGURATION_SAVE_PATH', default='./src/config/server.conf')

DEFAULT_HOST_NAME = os.getenv('DEFAULT_HOST_NAME', default='minechat.dvmn.org')

MAX_CONNECTION_ATTEMPT_RETRY = 5
CONNECTION_RETRY_TIMEOUT_SEC = 2
SERVER_RESPOND_TIMEOUT_SEC = 1
