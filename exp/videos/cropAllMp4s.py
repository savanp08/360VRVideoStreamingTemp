import os
import subprocess

def get_video_duration(file_path):
    # FFmpeg command to get video duration
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

def crop_video(file_path, start_time, end_time):
    output_file = os.path.splitext(file_path)[0] + "_cropped.mp4"

    # FFmpeg command to crop the video
    ffmpeg_command = [
        "ffmpeg",
        "-i", file_path,
        "-ss", str(start_time),
        "-to", str(end_time),
        "-c:v", "copy",  # No re-encoding for video
        "-c:a", "copy",  # No re-encoding for audio
        output_file
    ]

    subprocess.run(ffmpeg_command)
    print(f"Cropped video: {file_path} -> {output_file}")

def process_videos(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            file_path = os.path.join(directory, filename)
            duration = get_video_duration(file_path)
            print(f"Duration of {filename}: {duration} seconds")

            if duration > 80:
                start_time = int(input("Enter start time in seconds: "))
                end_time = int(input("Enter end time in seconds: "))
                
                if 0 <= start_time < end_time <= duration:
                    crop_video(file_path, start_time, end_time)
                else:
                    print("Invalid time frame. Please ensure start time is less than end time and within video duration.")

# Usage
process_videos("./")
