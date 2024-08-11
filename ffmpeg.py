import subprocess

def merge_video_audio(video_file, audio_file, output_file):
    command = [
        'ffmpeg',
        '-y',  # Overwrite output file if it exists
        '-i', video_file,
        '-i', audio_file,
        '-map', '0:v',  # Use video stream from the first input (video_file)
        '-map', '1:a',  # Use audio stream from the second input (audio_file)
        '-c:v', 'copy',  # Copy the video stream without re-encoding
        '-c:a', 'aac',  # Encode audio with AAC codec
        '-shortest',  # Stop encoding when the shortest input ends
        output_file
    ]
    subprocess.run(command, check=True)
