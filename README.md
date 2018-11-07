# Oak

Oak is aimed to be a simple discord bot for organizing EX raids channels.

## Features

- Welcome message to new Discord members
- Automatic raid entry to a monocle database based on a submitted screenshot (requires Google Vision API key)
- Automatic quest entry to a monocle database based on a submitted screenshot + pokemon name (requires Google Vision API key)
- Allow user to automatically join a 'sector role'

## Requirements

- Python version 3.4 between 3.6. **Python 3.7 is not suported.**

## Setting up

1. `pip3 install -r requirements.txt`
2. Put your bot token in a `token` file (follow [these instructions](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) to create a bot and get the token).
3. Copy `example_config.py` to `configuration.py` and edit all IDs and values to fit your Discord server and your database
4. If you need image-to-text, sign up for a [Google Vision](https://cloud.google.com/vision/) API key and export with the command `export GOOGLE_APPLICATION_CREDENTIALS=~/google-vision-key.json`
5. Run `python3 oak.py`
