# Telegram Bot

Send data through the telegram bot API. Currently, supports sending messages
and photos.

## Installation

Install with pip

```
pip install ciresbot
```

## Usage

### Python Module

Creating a bot requires only its token. To send messages or photos it needs
to know the chat id of the recipient(s) (see below how to obtain the chat ids).

```python
from telegrambot import TelegramBot

bot = TelegramBot("MyBotToken")
bot.send_message("Hello World", chat_id="12345")
bot.send_photo("./dog.jpg", caption="Cute dog", chat_id="12345")
```

Ideally, the token bot should not be hardcoded, the module also comes with some utilities
to read your tokens from a file. It expects a csv file with the following format:

```csv
# tokens.csv
botName,token
MyBot,MyBotToken12345
```

Also, you can read your chats from a csv file:

```csv
chatName,chatId,bot
MyChat,12345,MyBot
```

If you have a file with the above specifications you can use the utility functions
as in the following example:

```python
from telegrambot import TelegramBot
from telegrambot.utils import read_token_file, get_chat_id

token = read_token_file("./tokens.csv", "MyBot")
if not token:
   raise ValueError("Token not found")
    
chat_id = get_chat_id("MyChat", "./chats.csv")
if not chat_id:
    raise ValueError("Chat id not found")

bot = TelegramBot(token)
success, status_code, message = bot.send_message("Hello", chat_id)
if success:
    print(f"Message sent successfully: {message}")
else:
    print(f"Failed to send message {status_code}")
```

### Command Line Tool

The command line tool supports the following modes:

- `message`: Send a text message through Telegram using a bot.
- `photo`: Send a photo through Telegram using a bot.
- `updates`: Get the latest updates of the bot from Telegram.

### Options

Common options that can be used with all modes:

- `--bot, -b`: Name or token of the bot that will be used (required).
- `--token, -t`: Whether a token was passed. If not, it is assumed that the bot name was passed.
- `--bot-file, -f`: Name of the CSV file containing the token(s) of the bot(s). Required if the bot name was passed.
- `--chat, -c`: Name or ID of the chat where the info will be sent (required).
- `--id, -i`: Whether a chat ID was passed. If not, it is assumed that the chat name was passed.
- `--chat-file, -cf`: Name of the CSV file containing the ID(s) of the chat(s). Required if the bot name was passed.

Specific options for each mode:

#### Message Mode

- `--message, -m`: Text of the message (required).

#### Photo Mode

- `--photo, -p`: Path to the photo file (required).
- `--caption, -cp`: A caption for the photo (optional).

### Examples

Sending a message using a bot:

```shell
telegrambot message --bot MyBot --message "Hello, World!" --chat MyChat --bot-file ./bot.csv --chat-file ./chat.csv
```

Sending a photo using a bot:

```shell
telegrambot photo --bot MyBot --photo ./photo.jpg --caption "A picture" --chat MyChat --bot-file ./bot.csv --chat-file ./chat.csv
```

Getting updates of a bot 

```shell
telegrambot updates --bot MyBot --bot-file ./bot.csv
```

### Obtaining chat ids

To obtain the chat id, first add the bot to a new chat or an existing one. Then send a message to the
chat. Wait a few seconds and after that get the updates of the bot, you can use the CLI. In the updates
the chat id will appear.

## License

Created by Daniel Ibarrola. It is licensed under the terms of the MIT license.