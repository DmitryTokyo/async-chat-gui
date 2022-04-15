import json
import logging

from config import save_user_info
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
        raise HashError

    if upd_user_file:
        save_user_info(response)
