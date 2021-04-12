# MINECRAFT CHAT

[![license](https://img.shields.io/github/license/DAVFoundation/captain-n3m0.svg?style=flat-square)](https://github.com/DmitryTokyo/minecraft-chat/blob/master/LICENSE)

## Installation

For correct microservice work needs Python not less 3.8 version. I recommend to use virtual environment. All dependencies you should set from requirements.txt by command:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python server.py arguments

python client.py arguments
```

The service support the next arguments:

- --host - an IP address or address of host.
- --port_out - port for reading messages.
- --server - save your server configuration to config file.
- --user_hash - user account hash.
- --port_in - port for sending messages.
- --nickname - your chat nickname.
- --user_conf - save user configuration to file.

Also you can set argument by putting the environment variables in a config file, for example `config.ini`. The config file syntax - key=value.

## Files

`server.py` - server side script.
`client` - client side script.
`config.py` - start arguments configurations.

## License
