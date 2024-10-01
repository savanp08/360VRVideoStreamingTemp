import os
import subprocess

def convert_mov_to_mp4(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".mov"):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, os.path.splitext(filename)[0] + ".mp4")

            # FFmpeg command to convert MOV to MP4 with H.264 codec
            ffmpeg_command = [
                "ffmpeg",
                "-i", input_file,
                "-c:v", "libx264",
                "-c:a", "aac",  # Use AAC for audio encoding
                "-strict", "experimental",
                "-b:a", "192k",  # Audio bitrate
                output_file
            ]

            subprocess.run(ffmpeg_command)
            print(f"Converted: {input_file} -> {output_file}")

# Usage
convert_mov_to_mp4("./")
