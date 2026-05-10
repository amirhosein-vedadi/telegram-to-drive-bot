"""
Telegram-to-Google-Drive Bot

A lightweight bot that receives files (documents, videos, audio, photos, etc.)
from you on Telegram and saves them to a Google Drive folder.

Usage:
    python main.py

Configuration:
    Set BOT_TOKEN, API_ID, and API_HASH before running.
    For Colab: use colab_notebook.ipynb instead.

Supported file types:
    Documents, videos, audio files, voice messages, photos, animated GIFs.
"""

import os
import time
import shutil
import asyncio
from datetime import datetime
from dotenv import load_dotenv

from pyrogram import Client, filters, idle
from pyrogram.types import Message

# Load environment variables from .env file
load_dotenv()

# ============================================================
# CONFIGURATION
# Replace these values with your own credentials.
# - BOT_TOKEN: Get from @BotFather on Telegram
# - API_ID & API_HASH: Get from https://my.telegram.org
# ============================================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
API_ID = int(os.getenv("API_ID", 0))  # Convert to int!
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH_HERE")

DRIVE_FOLDER = "/content/drive/MyDrive/TelegramUploads"
TEMP_FOLDER = "/content/tmp_telegram_uploads"

os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(DRIVE_FOLDER, exist_ok=True)

app = Client(
    "telegram_drive_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# ============================================================
# HELPERS
# ============================================================

def safe_filename(name: str) -> str:
    """Remove characters that are invalid or problematic in filenames."""
    bad_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
    for ch in bad_chars:
        name = name.replace(ch, "_")
    return name.strip()


def make_unique_name(original_name: str) -> str:
    """Append a timestamp to guarantee uniqueness."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{ts}_{original_name}"


def get_message_file_name(message: Message) -> str:
    """Extract a sensible filename from the incoming Telegram message."""
    if message.document:
        return message.document.file_name or "file"
    if message.video:
        return "video.mp4"
    if message.audio:
        return message.audio.file_name or "audio.mp3"
    if message.voice:
        return "voice.ogg"
    if message.photo:
        return "photo.jpg"
    if message.animation:
        return "animation.mp4"
    return "file"


# ============================================================
# HANDLERS
# ============================================================

@app.on_message(filters.private & (
    filters.document | filters.video | filters.audio |
    filters.voice | filters.photo | filters.animation
))
async def handle_file(client, message: Message):
    """Download an incoming file and save it to Google Drive."""
    try:
        user = message.from_user
        user_id = user.id if user else "unknown"

        original_name = get_message_file_name(message)
        original_name = safe_filename(original_name)
        final_name = make_unique_name(original_name)

        temp_path = os.path.join(TEMP_FOLDER, final_name)
        drive_path = os.path.join(DRIVE_FOLDER, final_name)

        # Send a liveness indicator so the user knows we received the file
        await message.reply_text("Processing your file... ⏳")

        # Download file to temp location
        await message.download(file_name=temp_path)

        # Move to Google Drive folder
        shutil.move(temp_path, drive_path)

        # Success response
        text = (
            f"✅ File saved successfully.\n\n"
            f"📄 Name: `{final_name}`\n"
            f"📁 Path in Drive:\n`{drive_path}`\n"
            f"👤 User ID: `{user_id}`"
        )
        await message.reply_text(text, parse_mode="markdown")

    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error processing file: {e}")
        await message.reply_text(f"❌ Error processing file:\n`{e}`", parse_mode="markdown")


@app.on_message(filters.private & filters.command(["start", "help"]))
async def start_handler(client, message: Message):
    """Send a welcome message with usage instructions."""
    await message.reply_text(
        "👋 Hello! I'm your Telegram-to-Google Drive helper.\n\n"
        "Simply send me any file (document, video, photo, audio, voice)\n"
        "and I'll save it to your Google Drive.\n\n"
        "Supported types: Documents, Videos, Audio, Photos, Voice, GIFs."
    )


# ============================================================
# MAIN
# ============================================================

async def run_bot():
    """Start the bot and keep it running until interrupted."""
    print("Starting Telegram bot...")
    await app.start()
    print("Bot is running. Send me a file to save it to Google Drive.")
    try:
        await idle()
    except KeyboardInterrupt:
        print("\nShutting down bot...")
    finally:
        await app.stop()
        print("Bot stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except Exception as e:
        print(f"Fatal error: {e}")
