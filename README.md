# Telegram-Safe-Bot

[![Build Status](https://travis-ci.org/GabrielRF/Telegram-Safe-Bot.svg?branch=master)](https://travis-ci.org/GabrielRF/Telegram-Safe-Bot)

Telegram Bot available at www.telegram.me/Safe_Bot

## Instalation

Clone or download the repo. Then, run:

```
pip3 install -r requirements
```

Open the configuration sample file, edit it as you like and save as `bot.conf`:

### Parameters 

`TOKEN` = Bot Token. Given by [@BotFather](https://telegram.me/BotFather)

`START` = Start and Cancel message

`PASSWORD` = Password message

`HASH` = Hash message

`TEXT` = Message that asks for a text do calculate the hash

`SIZE` = Message that asks for the password size

`INFO` = Informations about the bot

## Run

```
python3 safe_bot.py
```
