import json
import logging

from config import update_user_config
from custom_error import HashError

logger = logging.getLogger(__file__)


async def authorize(reader, writer, user_hash, upd_user_file):
    response = await reader.readline()
    logger.debug(response.decode())

    writer.write(user_hash.encode())
    writer.write('\n\n'.encode())

    response = await reader.readline()
    logger.debug(response.decode())

    if not json.loads(response.decode()):
        print(f'User hash: {user_hash} is unknown. Please check or get a new one.')
        raise HashError

    if upd_user_file:
        update_user_config(response)
