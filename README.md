# MINECRAFT CHAT

[![license](https://img.shields.io/github/license/DAVFoundation/captain-n3m0.svg?style=flat-square)](https://github.com/DmitryTokyo/minecraft-chat/blob/master/LICENSE)

As you know all network communications goes through a socket. In this project you can look how socket works. There are 2 parts of simple chat application. First part is chat server. It server opens up port 5000 to listen for incoming connections. Second part is chat client. The client are listening user input and server message at same time. And if user input a message client send it to server.

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

```
--host      - an IP address or address of host.
--port_out  - port for reading messages.
--server    - save your server configuration to config file.
--user_hash - user account hash.
--port_in   - port for sending messages.
--nickname  - your chat nickname.
--user_conf - save user configuration to file.
```

Also you can set argument by putting the environment variables in a config file, for example `config.ini`. The config file syntax - `key=value`.

## Files overview

`server.py` - broadcasts all messages from other connected clients.

`client` - checks user input and in case if it is message then send it to server.

`config.py` - determines start arguments configuration.
