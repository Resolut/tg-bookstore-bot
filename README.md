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
