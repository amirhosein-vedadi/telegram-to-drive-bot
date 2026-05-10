# Telegram to Google Drive Bot

A lightweight Telegram bot that receives files from you on Telegram and automatically saves them to your Google Drive folder.

[![Run on Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirhosein-vedadi/telegram-to-drive-bot/blob/main/colab_notebook.ipynb)

## How it works

1. You message your Telegram bot with a file (document, video, photo, audio, voice, GIF)
2. The bot downloads the file and saves it to a specified Google Drive folder
3. The bot replies with the file name and Drive path for confirmation

## Supported file types

- Documents (PDFs, archives, etc.)
- Videos (MP4, etc.)
- Audio files (MP3, etc.)
- Voice messages
- Photos
- Animated GIFs

## Quick start (Google Colab)

The easiest way to run this bot is via Google Colab — no local setup required.

1. Click the **Run on Colab** badge above to open the notebook
2. Replace `YOUR_BOT_TOKEN_HERE`, `YOUR_API_ID_HERE`, and `YOUR_API_HASH_HERE` with your credentials
3. Run all cells (Runtime → Run all)
4. Message your bot on Telegram to start sending files

### Getting your credentials

| Credential | Where to get it |
|---|---|
| **Bot Token** | Message [@BotFather](https://t.me/BotFather) on Telegram, use `/newbot`, copy the token |
| **API ID** | Visit [my.telegram.org](https://my.telegram.org), log in, click "API development tools" |
| **API HASH** | Same page as API ID — shown together |

## Local setup

```bash
pip install -r requirements.txt

# Edit main.py and set your BOT_TOKEN, API_ID, and API_HASH
python main.py
```

Or use a `.env` file:

```bash
cp .env.example .env
# Edit .env with your credentials
```

## Notes

- The bot is **open to all** — anyone who messages it can send files
- Files are saved with a timestamp prefix to avoid collisions
- A temporary folder is used during download and cleaned up on move
- The Google Drive folder path is configurable in the code

## License

This project is provided as-is. Use at your own responsibility.
