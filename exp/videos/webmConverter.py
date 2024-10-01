import os
import subprocess

def convert_mp4_to_webm(folder_path):
    for root, _, files in os.walk(folder_path):
        print(f"Converting files in {root}")
        print(files)
        print(folder_path, root)
        if root == folder_path:
            print("Root is folder path")
            continue
        for file in files:
            if file.endswith(".mp4"):
                mp4_file = os.path.join(root, file)
                webm_file = os.path.splitext(mp4_file)[0] + ".webm"
                convert_to_webm(mp4_file, webm_file)

def convert_to_webm(input_file, output_file):
    try:
        subprocess.run(['ffmpeg', '-i', input_file, '-c:v', 'libvpx', '-b:v', '1M', '-c:a', 'libvorbis', output_file], check=True)
        print(f"Converted {input_file} to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert {input_file} to {output_file}: {e}")

# Example usage
base_folder = './video0'  # Change this to your relative folder path
convert_mp4_to_webm(base_folder)
