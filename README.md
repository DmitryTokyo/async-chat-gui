# MINECRAFT CHAT

## Installation

For correct microservice work needs Python not less 3.8 version. I recommend to use virtual environment. All dependencies you should set from requirements.txt by command:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 server.py arguments
```

The service support the next arguments:

- --host - an IP address or address of host.
- --port - host port
- --path - chat file path, for example `./chat.txt`.

Also you can set argument by putting the environment variables in a config file, for example `config.ini`. The config file syntax - key=value.
