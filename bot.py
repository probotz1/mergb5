from pyrogram import Client, filters
from pyrogram.types import Message
from ffmpeg import merge_video_audio
import os
import time

# API credentials
API_ID = "28015531"
API_HASH = "2ab4ba37fd5d9ebf1353328fc915ad28"
BOT_TOKEN = "7321073695:AAE2ZvYJg6_dQNhEvznmRCSsKMoNHoQWnuI"

app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    sleep_threshold=10
)

# Store video files for users
user_video = {}

def progress_bar(current, total, message: Message, action="Uploading"):
    percentage = current * 100 / total
    progress = int(percentage // 5)
    progress_message = f"{action}...\n\n" \
                       f"{'⬢' * progress}{'⬡' * (20 - progress)}\n\n" \
                       f"╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣\n" \
                       f"┣⪼ 🗃️ Sɪᴢᴇ: {current / 1048576:.2f} Mʙ | {total / 1048576:.2f} Mʙ\n" \
                       f"┣⪼ ⏳️ Dᴏɴᴇ : {percentage:.2f}%\n" \
                       f"┣⪼ 🚀 Sᴩᴇᴇᴅ: {current / 1024 / 1024 / (time.time() - start_time):.2f} Mʙ/s\n" \
                       f"┣⪼ ⏰️ Eᴛᴀ: {((total - current) / 1024 / 1024) / (current / 1024 / 1024 / (time.time() - start_time)):.0f}s\n" \
                       f"╰━━━━━━━━━━━━━━━➣"

    message.edit(progress_message)

@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    await message.reply("Welcome! Send me a video file to start the merging process.")

@app.on_message(filters.video)
async def video_handler(client, message: Message):
    user_video[message.from_user.id] = await message.download(progress=progress_bar, progress_args=(message, "Downloading Video"))
    await message.reply("Video downloaded. Now, please send the audio file you want to merge with the video.")

@app.on_message(filters.audio)
async def audio_handler(client, message: Message):
    user_id = message.from_user.id

    if user_id not in user_video:
        await message.reply("Please send a video file first.")
        return

    audio = await message.download(progress=progress_bar, progress_args=(message, "Downloading Audio"))
    video = user_video.pop(user_id)
    
    output_file = "output.mp4"
    merge_video_audio(video, audio, output_file)

    start_time = time.time()
    await message.reply_video(output_file, progress=progress_bar, progress_args=(message, "Uploading"))

    os.remove(video)
    os.remove(audio)
    os.remove(output_file)

    await message.delete()

if __name__ == "__main__":
    app.run()
