import configargparse


def get_config():
    parser = configargparse.ArgParser(default_config_files=['*.conf'])

    parser.add_argument('--host', type=str, help='host name', default='minechat.dvmn.org')
    parser.add_argument('--port_out', type=int, help='chat port out (server.py)', default=5000)
    parser.add_argument('--path', type=str, help='chat file path', default='./chat.txt')
    parser.add_argument('--server', action='store_true',
                        help='update server config file')

    parser.add_argument('--user_hash', type=str, help='user hash')
    parser.add_argument('--nickname', type=str, help='nickname')
    parser.add_argument('--port_in', type=int, help='chat port in (client.py)', default=5050)
    parser.add_argument('--user_conf', action='store_true', help='save user config')
    
    config, unknown = parser.parse_known_args()

    if config.server:
        update_server_config_file(config)
    return config


def update_server_config_file(config):
    with open('server.conf', 'w') as file:
        file.write(f'host={config.host}\n') 
        file.write(f'port_out={config.port_out}\n')
        file.write(f'port_in={config.port_in}\n')
        file.write(f'path={config.path}\n')