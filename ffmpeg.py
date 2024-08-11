import subprocess

def merge_video_audio(video_path, audio_path, output_path):
    """
    Merges a video file with an audio file, replacing the original audio.
    The output file will be saved to the provided output path.

    :param video_path: Path to the video file.
    :param audio_path: Path to the audio file.
    :param output_path: Path where the output file will be saved.
    """
    try:
        command = [
            'ffmpeg',
            '-y',  # Overwrite output file if it exists
            '-i', video_path,  # Input video file
            '-i', audio_path,  # Input audio file
            '-map', '0:v',  # Select the video stream from the first input
            '-map', '1:a',  # Select the audio stream from the second input
            '-c:v', 'copy',  # Copy the video stream (no re-encoding)
            '-c:a', 'aac',  # Encode audio to AAC format
            '-shortest',  # Stop encoding when the shortest input stream ends
            output_path  # Output file path
        ]

        subprocess.run(command, check=True)
        print(f"Successfully merged video and audio into {output_path}")
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while merging video and audio: {e}")
        raise e  # Re-raise the exception to handle it in the calling function
