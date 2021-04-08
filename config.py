import configargparse


def get_config():
    parser = configargparse.ArgParser(default_config_files=['config.ini'])
    parser.add_argument('--host', type=str, help='host')
    parser.add_argument('--port_out', type=int, help='chat port out')
    parser.add_argument('--port_in', type=int, help='chat port in')
    parser.add_argument('--path', type=str, help='chat file path')
    parser.add_argument('--user_hash', type=str, help='user hash')
    config, unknown = parser.parse_known_args()
    return config
