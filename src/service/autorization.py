import json

from src.config.chat_config import save_user_info
from src.custom_error import InvalidToken

from loguru import logger


async def authorize(reader, writer, user_hash, upd_user_file):
    user_hash_identification_response = await get_user_identification_response(reader, writer, user_hash)
    if not json.loads(user_hash_identification_response.decode()):
        logger.bind(
            module='client',
            action='authorisation',
            user_hash=user_hash,
            user_hash_identification=str(user_hash_identification_response.decode()),
        ).error('User identification response error')
        raise InvalidToken(user_hash)

    logger.bind(
        module='client',
        action='authorisation',
        user_hash=user_hash,
        user_hash_identification=str(user_hash_identification_response.decode()),
    ).debug('User identification response')
    if upd_user_file:
        save_user_info(user_hash_identification_response)


async def get_user_identification_response(reader, writer, user_hash):
    await reader.readline()
    writer.write(user_hash.encode())
    writer.write('\n\n'.encode())

    return await reader.readline()
