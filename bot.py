from pyrogram import Client, filters
from pyrogram.types import Message
from ffmpeg import merge_video_audio
import os
import time

# Replace these with your actual credentials
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

app = Client(
    "my_bot",
    api_id=28015531,
    api_hash=2ab4ba37fd5d9ebf1353328fc915ad28,
    bot_token=7321073695:AAE2ZvYJg6_dQNhEvznmRCSsKMoNHoQWnuI
)

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

@app.on_message(filters.command("merge"))
async def merge_handler(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.video or not message.reply_to_message.audio:
        await message.reply("Please reply to a video and an audio file to merge them.")
        return

    start_time = time.time()
    video = await message.reply_to_message.download(progress=progress_bar, progress_args=(message, "Downloading Video"))
    audio = await message.reply_to_message.download(progress=progress_bar, progress_args=(message, "Downloading Audio"))

    output_file = "output.mp4"
    merge_video_audio(video, audio, output_file)

    await message.reply_video(output_file, progress=progress_bar, progress_args=(message, "Uploading"))

    os.remove(video)
    os.remove(audio)
    os.remove(output_file)

    await message.delete()

if __name__ == "__main__":
    app.run()
