import os
import subprocess

def convert_mp4_to_webm(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.mp4'):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, os.path.splitext(filename)[0] + '.webm')
            
            # Construct the ffmpeg command
            command = [
                'ffmpeg',
                '-i', input_file,
                '-c:v', 'libvpx',
                '-crf', '7',  # Quality level (0-63), lower is better quality
                '-b:v', '1M',  # Bitrate (optional, can adjust as needed)
                '-c:a', 'libvorbis',  # Audio codec
                output_file
            ]
            
            # Execute the command
            subprocess.run(command, check=True)
            print(f"Converted {input_file} to {output_file}")

if __name__ == "__main__":
    directory = "./"  # Change this to your directory
    convert_mp4_to_webm(directory)
