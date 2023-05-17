import time

from src.data_types import WatchDogMessage
from src.config import settings


def generate_watchdog_logger_messages(watchdog_message: WatchDogMessage) -> str:
    timestamp = int(time.time())
    if watchdog_message == WatchDogMessage.TIMEOUT_ELAPSED:
        return f'[{timestamp}] {settings.SERVER_RESPOND_TIMEOUT_SEC}s {watchdog_message.value}'

    return f'[{timestamp}] Connection is alive. {watchdog_message.value}'
