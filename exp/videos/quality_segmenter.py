import os
import subprocess
import random
import shutil

# Define the input directory and the output directories
relativeInputPath = './'
outputPath = {
    'good': '/good',
    'moderate': '/moderate',
    'low': '/low'
}

# Bitrate levels in kbps
bitrates = {
    'good': [4300, 3200, 2350, 1850, 1200, 750, 300],
    'moderate': [4300, 3200, 2350, 1850, 1200, 750, 300],
    'low': [4300, 3200, 2350, 1850, 1200, 750, 300],
}

# Target average bitrates for different qualities in kbps
target_avrg_bitrates = {
    'good': 3200,
    'moderate': 2100,
    'low': 900
}

# Resolution percentages for different qualities
resolutions = {
    'good': [100, 75, 50, 33.33, 33.33, 25, 16.67],
    'moderate': [100, 75, 50, 33.33, 33.33, 25, 16.67],
    'low': [100, 75, 50, 33.33, 33.33, 25, 16.67]
}

def ensure_even(value):
    return value if value % 2 == 0 else value - 1

def get_video_info(file_path):
    """Get video resolution using ffprobe"""
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', file_path]
    output = subprocess.check_output(cmd).decode().strip()
    width, height = map(int, output.split(','))
    return width, height

def process_segment(input_path, output_path, target_bitrate, resolution_percentage):
    width, height = get_video_info(input_path)
    width_thisQuality = ensure_even(width * resolution_percentage // 100)
    height_thisQuality = ensure_even(height * resolution_percentage // 100)
    target_bitrate = str(target_bitrate) + 'k'

    cmd = [
        'ffmpeg', '-i', input_path, '-vf', f'scale={width_thisQuality}:{height_thisQuality}',
        '-b:v', target_bitrate, '-minrate', target_bitrate, '-maxrate', target_bitrate, '-bufsize', target_bitrate,
        '-y', output_path
    ]
    subprocess.run(cmd)

def generate_bitrate_array(target_average, num_segments, allowed_bitrates):
    """Generate a bitrate array and adjust it until the average is close to the target."""
    selected_bitrates = []
    
    while True:
        selected_bitrates = [random.choice(allowed_bitrates) for _ in range(num_segments)]
        current_average = sum(selected_bitrates) / num_segments
        tolerance = 150  # Tolerance level
        if target_average == 2100:
            tolerance = 100
        elif target_average == 900:
            tolerance = 75
        if current_average - target_average < tolerance:  # Tolerance level
            break

        # Adjust the array to bring the average closer to the target
        for i in range(num_segments):
            if current_average < target_average:
                if selected_bitrates[i] < max(allowed_bitrates):
                    selected_bitrates[i] = min([b for b in allowed_bitrates if b > selected_bitrates[i]])
            else:
                if selected_bitrates[i] > min(allowed_bitrates):
                    selected_bitrates[i] = max([b for b in allowed_bitrates if b < selected_bitrates[i]])

        current_average = sum(selected_bitrates) / num_segments

    return selected_bitrates

def get_bitrate(file_path):
    """Get the bitrate of a video segment using ffprobe"""
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=bit_rate', '-of', 'csv=p=0', file_path]
    output = subprocess.check_output(cmd).decode().strip()
    return int(output) // 1000  # Convert from bps to kbps

def log_info(output_dir, quality, bitrates):
    log_file = os.path.join(output_dir, 'log.txt')
    average_bitrate = sum(bitrates) / len(bitrates)
    with open(log_file, 'w') as f:
        f.write(f"Quality: {quality}\n")
        f.write("Bitrates for each segment (kbps):\n")
        for bitrate in bitrates:
            f.write(f"{bitrate} kbps\n")
        f.write(f"Average bitrate achieved: {average_bitrate} kbps\n")

def main(relativePath, outputPathParam):
    outputPath = {
    'good': '/good',
    'moderate': '/moderate',
    'low': '/low'
    }
    relativeInputPath = relativePath
    for quality, output_dir in outputPath.items():
        outputPath[quality] = outputPathParam + output_dir
        print(output_dir)
    if not os.path.exists(relativeInputPath):
        print(f"Input directory '{relativeInputPath}' does not exist.")
        return

    for quality, output_dir in outputPath.items():
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        else:
            print(f"Creating directory '{output_dir}'")
        os.makedirs(output_dir)

    segments = [f for f in os.listdir(relativeInputPath) if f.endswith('.mp4')]
    num_segments = len(segments)

    for quality in ['good', 'moderate', 'low']:
        selected_bitrates = generate_bitrate_array(target_avrg_bitrates[quality], num_segments, bitrates[quality])
        resolution_percentages = [resolutions[quality][bitrates[quality].index(b)] for b in selected_bitrates]
        bitrates_for_logging = []

        for i, segment in enumerate(segments):
            input_path = os.path.join(relativeInputPath, segment)
            output_path = os.path.join(outputPath[quality], segment)
            process_segment(input_path, output_path, selected_bitrates[i], resolution_percentages[i])
            actual_bitrate = get_bitrate(output_path)
            bitrates_for_logging.append(actual_bitrate)

        log_info(outputPath[quality], quality, bitrates_for_logging)

# if __name__ == '__main__':
#     main()
