import argparse
from argparse import Namespace, ArgumentParser

import configargparse
import json

from src.config import settings


def get_chat_config() -> Namespace:
    server_config = get_server_config()
    client_config = get_client_config()

    chat_config = argparse.Namespace(**vars(server_config), **vars(client_config))

    return chat_config


def get_server_config() -> Namespace | None:
    base_parser = get_base_parser()
    parser = configargparse.ArgParser(
        default_config_files=[settings.SERVER_CONFIGURATION_FILE_PATH],
        parents=[base_parser],
    )

    parser.add_argument('--port-out', type=int, help='chat port out in server module', default=5000)
    parser.add_argument('--history-path', type=str, help='chat file path', default=settings.CHAT_HISTORY_SAVE_PATH)
    parser.add_argument('--save-config', action='store_true', help='save server configuration to file')
    
    config, unknown = parser.parse_known_args()

    if not config.host or not config.port_out:
        parser.error('You should to text host name (--host) and port (--port_out)')

    if config.save_config:
        save_server_configuration(config)
    return config


def get_client_config() -> Namespace | None:
    parser = configargparse.ArgParser(default_config_files=[settings.USER_CONFIGURATION_FILE_PATH])
    parser.add_argument('--user-hash', type=str, help='user hash')
    parser.add_argument('--nickname', type=str, help='nickname')
    parser.add_argument('--port-in', type=int, help='chat port in', default=5050)
    parser.add_argument('--save-info', action='store_true', help='save client information to file')
    config, unknown = parser.parse_known_args()
    return config


def get_base_parser() -> ArgumentParser:
    parser = configargparse.ArgParser(add_help=False)
    parser.add_argument('--host', type=str, help='host name', default=settings.DEFAULT_HOST_NAME)
    return parser


def save_server_configuration(server_config: Namespace) -> None:
    with open(settings.SERVER_CONFIGURATION_FILE_PATH, 'w') as file:
        file.write(f'host={server_config.host}\n')
        file.write(f'port_out={server_config.port_out}\n')
        file.write(f'history_path={server_config.history_path}\n')
        

def save_user_info(response):
    user_info = json.loads(response.decode())

    with open(settings.USER_CONFIGURATION_FILE_PATH, 'w') as file:
        file.write(f'user-hash={user_info["account_hash"]}\n')
        file.write(f'nickname={user_info["nickname"]}\n')