import os
import subprocess

# Define the bitrates for different qualities
relative_bitrates = [
    {"id": "video2", "fraction": 0.8},   # 20% of original quality
    {"id": "video3", "fraction": 0.6},   # 30% of original quality
    {"id": "video4", "fraction": 0.5},   # 50% of original quality
    {"id": "video5", "fraction": 0.4},  # 75% of original quality
    {"id": "video6", "fraction": 0.25},    # 100% of original quality
    {"id": "video7", "fraction": 0.2}    # 100% of original quality
]

# Define the paths
input_folder = os.getcwd()  # Current directory
output_folder = os.getcwd()  # Current directory, but can be changed if needed

# Function to get the bitrate of a video using ffprobe
def get_video_bitrate(video_path):
    cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -of csv=p=0 {video_path}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    bitrate = int(result.stdout.strip())
    return bitrate

# Function to get the resolution of a video using ffprobe
def get_video_resolution(video_path):
    cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {video_path}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    width, height = map(int, result.stdout.strip().split('x'))
    return width, height

# Get the list of .mp4 files in the current directory
mp4_files = [f for f in os.listdir(input_folder) if f.endswith(".mp4")]

# Process each .mp4 file
for mp4_file in mp4_files:
    input_video = os.path.join(input_folder, mp4_file)
    original_width, original_height = get_video_resolution(input_video)
    original_bitrate = get_video_bitrate(input_video)

    # Calculate the bitrates and resolutions for different qualities
    for bitrate in relative_bitrates:
        bitrate["bandwidth"] = int(original_bitrate * bitrate["fraction"])
        bitrate["width"] = int(original_width * bitrate["fraction"])
        bitrate["height"] = int(original_height * bitrate["fraction"])

        # Ensure the width and height are even numbers
        if bitrate["width"] % 2 != 0:
            bitrate["width"] += 1
        if bitrate["height"] % 2 != 0:
            bitrate["height"] += 1

    # Create the output directories if they do not exist
    for bitrate in relative_bitrates:
        os.makedirs(os.path.join(output_folder, bitrate["id"]), exist_ok=True)

    # Generate the converted videos using FFmpeg
    for bitrate in relative_bitrates:
        output_dir = os.path.join(output_folder, bitrate["id"])
        output_file = os.path.join(output_dir, mp4_file)
        cmd = (
            f"ffmpeg -i {input_video} -b:v {bitrate['bandwidth']} -vf scale={bitrate['width']}:{bitrate['height']} "
            f"-c:v libx264 -preset fast -crf 23 -c:a copy {output_file}"
        )
        subprocess.run(cmd, shell=True)
        print(f"Created {output_file} with bitrate {bitrate['bandwidth']} and resolution {bitrate['width']}x{bitrate['height']}")
