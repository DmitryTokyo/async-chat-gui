import json
import logging

from src.config import save_user_info
from src.utils.custom_error import HashError

logger = logging.getLogger(__file__)


async def authorize(reader, writer, user_hash, upd_user_file):
    user_hash_identification_response = await get_user_identification_response(reader, writer, user_hash)
    logger.debug(user_hash_identification_response.decode())

    if not json.loads(user_hash_identification_response.decode()):
        raise HashError

    if upd_user_file:
        save_user_info(user_hash_identification_response)


async def get_user_identification_response(reader, writer, user_hash):
    response = await reader.readline()
    logger.debug(response.decode())

    writer.write(user_hash.encode())
    writer.write('\n\n'.encode())

    return await reader.readline()
