"""
File: frames_to_video_12bit.py
Author: Isaac Monheit
Date: 1/29/24
Description: Converts a folder of 16-bit frames into one 12-bit compressed video using FFmpeg (failed attempt at 16-bit video)

             Currently is a WIP on 16 big video compression using ffmpeg and VVC combo, not getting a ton of luck
"""

import subprocess
import os

# Set your parameters
frame_rate = 30  # or whatever your frame rate is
input_folder = 'capture'  # make sure this is the path to your images
output_file = 'videos/test1_16bit.mp4'  # your desired output file
resolution = "640x512"

# Construct the FFmpeg command as a string
# command = f'ffmpeg -framerate {frame_rate} -i {input_folder}/neutrino_capture%d.png -c:v libx265 -x265-params lossless=1 -pix_fmt yuv420p16le {output_file}'
# subprocess.run(command, shell=True)

# command = f'ffmpeg -f rawvideo -vcodec rawvideo -s {resolution} -framerate {frame_rate} -pix_fmt gray16le -i {input_folder}/neutrino_capture%d.png -an -vcodec vvc {output_file}'
command = f'ffmpeg -r {frame_rate} -i {input_folder}/neutrino_capture%d.png -pix_fmt gray16be -an -vcodec vvc -vvenc-params bitrate=1M:passes=2:pass=1 {output_file}'
subprocess.run(command, shell=True)


#################### NEW TEST WITH FFMPEG AND VVC COMBO ###################################
# Construct the FFmpeg command as a string for VVC
# command = [
#     'ffmpeg',
#     '-framerate', str(frame_rate),
#     '-i', f'{input_folder}/neutrino_capture0.png',  # input frames pattern
#     '-an',  # no audio
#     '-vcodec', 'vvc',  # specify VVC codec
#     '-vvenc-params', 'bitrate=1M:passes=2:pass=1',  # VVC specific parameters
#     output_file  # output file
# ]

# subprocess.run(command)

# Calculate the size of the input folder
input_folder_size = sum(os.path.getsize(os.path.join(input_folder, filename)) for filename in os.listdir(input_folder))

# Calculate the size of the output video
output_video_size = os.path.getsize(output_file)

# Print the sizes
print(f"Size of input folder: {input_folder_size / (1024 * 1024):.2f} MB")
print(f"Size of output video: {output_video_size / (1024 * 1024):.2f} MB")
