import configargparse
import json


def get_server_config():
    base_parser = get_base_parser()
    parser = configargparse.ArgParser(default_config_files=['server.conf'], parents=[base_parser])

    parser.add_argument('--port_out', type=int, help='chat port out (server.py)', default=5000)
    parser.add_argument('--path', type=str, help='chat file path', default='./chat.txt')
    parser.add_argument('--save_config', action='store_true', help='save server configuration to file')
    
    config, unknown = parser.parse_known_args()

    if not config.host or not config.port_out:
        parser.error('You should to text host name (--host) and port (--port_out)')

    if config.save_config:
        save_server_configuration(config)
    return config


def get_client_config():
    base_parser = get_base_parser()
    parser = configargparse.ArgParser(default_config_files=['user.conf'], parents=[base_parser])
    parser.add_argument('--user_hash', type=str, help='user hash')
    parser.add_argument('--nickname', type=str, help='nickname')
    parser.add_argument('--port_in', type=int, help='chat port in (client.py)', 
                        default=5050)
    parser.add_argument('--save_info', action='store_true',
                        help='save client information to file')
    config, unknown = parser.parse_known_args()
    return config


def get_base_parser():
    parser = configargparse.ArgParser(add_help=False)
    parser.add_argument('--host', type=str, help='host name', 
                        default='minechat.dvmn.org')
    return parser


def save_server_configuration(config):
    with open('server.conf', 'w') as file:
        file.write(f'host={config.host}\n') 
        file.write(f'port_out={config.port_out}\n')
        file.write(f'path={config.path}\n')
        

def save_user_info(response):
    user_info = json.loads(response.decode())

    with open('user.conf', 'w') as file:
        file.write(f'user_hash={user_info["account_hash"]}\n')
        file.write(f'nickname={user_info["nickname"]}\n')