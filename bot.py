from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import time
import os
from ffmpeg import merge_video_audio

API_ID = "28015531"
API_HASH = "2ab4ba37fd5d9ebf1353328fc915ad28"
BOT_TOKEN = "7321073695:AAE2ZvYJg6_dQNhEvznmRCSsKMoNHoQWnuI"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

progress_message_id = {}

async def send_progress_message(client: Client, chat_id: int, text: str):
    """Send a progress message and store its message ID."""
    global progress_message_id

    if chat_id in progress_message_id:
        try:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=progress_message_id[chat_id],
                text=text
            )
        except Exception as e:
            print(f"Error editing message: {e}")
            # Clear the stored message ID if it's invalid
            progress_message_id.pop(chat_id, None)
            # Send a new progress message
            new_message = await client.send_message(
                chat_id=chat_id,
                text=text
            )
            progress_message_id[chat_id] = new_message.message_id
    else:
        new_message = await client.send_message(
            chat_id=chat_id,
            text=text
        )
        progress_message_id[chat_id] = new_message.message_id

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("Send a video file.")

@app.on_message(filters.video)
async def video_handler(client: Client, message: Message):
    video_file = await message.download()  # Download video file
    await message.reply_text("Video received. Please send an audio file.")

@app.on_message(filters.audio)
async def audio_handler(client: Client, message: Message):
    audio_file = await message.download()  # Download audio file
    video_file = "path_to_downloaded_video"  # Ensure this points to the downloaded video file

    output_file = "output.mp4"

    try:
        merge_video_audio(video_file, audio_file, output_file)
        await message.reply_document(output_file)
    except Exception as e:
        error_message = f"An error occurred during merging: {e}"
        await message.reply_text(error_message)
        print(error_message)

@app.on_message(filters.media)
async def handle_media(client: Client, message: Message):
    """Handle media progress and provide updates."""
    if message.video or message.audio:
        progress_text = f"Processing {message.file_name}..."
        await send_progress_message(client, message.chat.id, progress_text)

app.run()
