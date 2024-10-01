import subprocess
import os

def convert_video_to_keyframes(video_path, output_path):
    # Create the command to convert the video with keyframes at every 8 frames
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vcodec", "libx264",
        "-x264-params", "keyint=20:scenecut=0",
        "-acodec", "copy",
        output_path
    ]
    
    # Run the command
    subprocess.run(command, check=True)

import os
import subprocess

def split_video_exact_segments(video_path, output_dir, segment_length=4, max_segments=17):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create a temporary output pattern
    temp_output_pattern = os.path.join(output_dir, "temp_%d.mp4")

    # Create the command to split the video
    command = [
        "ffmpeg",
        "-i", video_path,
        "-c", "copy",
        "-f", "segment",
        "-segment_time", str(segment_length),
        "-reset_timestamps", "1",
        "-force_key_frames", "expr:gte(t,n_forced*{})".format(segment_length),
        temp_output_pattern
    ]
    
    # Run the command
    subprocess.run(command, check=True)
    
    # Rename the segments to start from 1 instead of 0 and limit to max_segments
    for filename in sorted(os.listdir(output_dir)):
        if filename.startswith("temp_") and filename.endswith(".mp4"):
            # Extract the original index from the filename
            original_index = int(filename.split('_')[1].split('.')[0])
            if original_index >= max_segments:
                os.remove(os.path.join(output_dir, filename))
            else:
                old_file = os.path.join(output_dir, filename)
                new_file = os.path.join(output_dir, "{}.mp4".format(original_index + 1))
                os.rename(old_file, new_file)
                print(f"Renamed {old_file} to {new_file}")


# # Example usage
# original_video_path = "input.mp4"
# keyframe_video_path = "inputfames.mp4"
# segments_output_dir = "output_segments"

# # Step 1: Convert the video to have keyframes at every 8 frames
# convert_video_to_keyframes(original_video_path, keyframe_video_path)

# # Step 2: Split the converted video into exact segments
# split_video_exact_segments(keyframe_video_path, segments_output_dir)