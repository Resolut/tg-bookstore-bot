[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## This is Telegram bot for the study fictional bookstore

## Dev guide
### How to run the project

1. Install `uv` (package manager) according these steps: https://docs.astral.sh/uv/getting-started/installation/

   uv docs: https://docs.astral.sh/uv/
1. Sync project requirements by command:
    ```bash
    uv sync
    ```
1. Create and get Bot token from `BotFather` bot in Telegram
   - type it in Telegram search field
   - choose `/newbot` in the bot commands menu and follow next steps

1. Create file `.env` in the project root directory with next content:
    ```
    BOT_TOKEN='<PASTE_YOUR_BOT_TOKEN>'
    DEBUG_MODE=1
    ```
1. Done! Your bot ready to run, execute `main` module as script and have a nice coding!
