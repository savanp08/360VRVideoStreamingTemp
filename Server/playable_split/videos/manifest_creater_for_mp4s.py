import os
import subprocess
from lxml import etree

# Function to get video details using ffprobe
def get_video_details(video_path):
    cmd = (
        f"ffprobe -v error -select_streams v:0 "
        f"-show_entries stream=width,height,bit_rate,r_frame_rate "
        f"-of csv=p=0 {video_path}"
    )
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    width, height, bit_rate, frame_rate = result.stdout.strip().split(',')
    width = int(width)
    height = int(height)
    # Handle potential non-integer bit_rate (e.g., "N/A" or frame rate appearing in bit_rate)
    try:
        bit_rate = int(bit_rate)
    except ValueError:
        bit_rate_cmd = (
            f"ffprobe -v error -select_streams v:0 -show_entries format=bit_rate "
            f"-of csv=p=0 {video_path}"
        )
        bit_rate_result = subprocess.run(bit_rate_cmd, shell=True, capture_output=True, text=True)
        bit_rate = int(bit_rate_result.stdout.strip())

    if '/' in frame_rate:
        frame_rate_num, frame_rate_den = map(int, frame_rate.split('/'))
        frame_rate = frame_rate_num / frame_rate_den
        frame_rate = f"{frame_rate_num}/{frame_rate_den}"
    else:
        frame_rate = f"{frame_rate}/1"
    return width, height, bit_rate, frame_rate

# Define paths and folders
input_folder = os.getcwd()
video_folders = [f"video{i}" for i in range(1, 8)]

# Collect video details
video_details = []
for folder in video_folders:
    video_path = os.path.join(input_folder, folder, "0.mp4")
    if os.path.exists(video_path):
        width, height, bit_rate, frame_rate = get_video_details(video_path)
        video_details.append({
            "id": folder,
            "width": width,
            "height": height,
            "bit_rate": bit_rate,
            "frame_rate": frame_rate
        })

# Function to create the MPD file
def create_mpd(video_details, output_path):
    MPD = etree.Element(
        "MPD",
        xmlns="urn:mpeg:dash:schema:mpd:2011",
        profiles="urn:mpeg:dash:profile:isoff-live:2011",
        type="static",
        minBufferTime="PT5.000S",
        maxSegmentDuration="PT2.005S",
        availabilityStartTime="2016-01-20T21:10:02Z",
        mediaPresentationDuration="PT193.680S"
    )

    period = etree.SubElement(MPD, "Period", id="period0")
    adaptation_set = etree.SubElement(
        period,
        "AdaptationSet",
        mimeType="video/mp4",
        segmentAlignment="true",
        startWithSAP="1",
        maxWidth=str(max(detail["width"] for detail in video_details)),
        maxHeight=str(max(detail["height"] for detail in video_details)),
        maxFrameRate="30000/1001",
        par="1:1"
    )

    segment_template = etree.SubElement(
        adaptation_set,
        "SegmentTemplate",
        timescale="90000",
        initialization="$RepresentationID$/Header.mp4",
        media="$RepresentationID$/$Number$.mp4",
        startNumber="1",
        duration="359408",
        presentationTimeOffset="0"
    )

    for detail in video_details:
        etree.SubElement(
            adaptation_set,
            "Representation",
            id=detail["id"],
            bandwidth=str(detail["bit_rate"]),
            codecs="avc1.4D401E",
            width=str(detail["width"]),
            height=str(detail["height"]),
            frameRate=detail["frame_rate"],
            sar="1:1",
            scanType="progressive"
        )

    tree = etree.ElementTree(MPD)
    tree.write(output_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")

# Create the manifest.mpd file
create_mpd(video_details, os.path.join(input_folder, "manifest.mpd"))

print("Manifest.mpd file has been created successfully.")
