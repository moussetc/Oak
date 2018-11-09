# Oak

Oak is aimed to be a simple discord bot for organizing EX raids channels.

## Features

- Welcome message to new Discord members
- Automatic raid entry to a monocle database based on a submitted screenshot (requires Google Vision API key)
- Automatic quest entry to a monocle database based on a submitted screenshot + pokemon name (requires Google Vision API key)
- Allow user to automatically join a 'sector role'

## Requirements

- Tests have been made with Python version 3.5.2. Other versions may be compatible, but because of discord.py, **Python 3.7 is not supported.**

## Setting up

1. Put your bot token in a `token` file (follow [these instructions](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) to create a bot and get the token).
2. Copy `example_config.py` to `configuration.py` and edit all IDs and values to fit your Discord server and your database
3. If you need image-to-text, sign up for a [Google Vision](https://cloud.google.com/vision/) API key and export with the command `export GOOGLE_APPLICATION_CREDENTIALS=~/google-vision-key.json`
4. Install the required package with `pip3 install -r requirements.txt` or (`pipenv install` if you're using [Pipenv](https://pipenv.readthedocs.io/en/latest/)).
5. Run `python3 oak.py` (or `pipenv run python oak.py`)
