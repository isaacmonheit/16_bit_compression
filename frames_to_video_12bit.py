"""
File: frames_to_video_12bit.py
Author: Isaac Monheit
Date: 1/29/24
Description: Converts a folder of 16-bit frames into one 12-bit video using FFmpeg (failed attempt at 16-bit video)
"""

import subprocess
import os

# Set your parameters
frame_rate = 30  # or whatever your frame rate is
input_folder = 'capture'  # make sure this is the path to your images
output_file = 'videos/test1_16bit.mp4'  # your desired output file

# Construct the FFmpeg command as a string
command = f'ffmpeg -framerate {frame_rate} -i {input_folder}/neutrino_capture%d.png -c:v libx265 -x265-params lossless=1 -pix_fmt yuv420p16le {output_file}'

# Run the command
subprocess.run(command, shell=True)

# Calculate the size of the input folder
input_folder_size = sum(os.path.getsize(os.path.join(input_folder, filename)) for filename in os.listdir(input_folder))

# Calculate the size of the output video
output_video_size = os.path.getsize(output_file)

# Print the sizes
print(f"Size of input folder: {input_folder_size / (1024 * 1024):.2f} MB")
print(f"Size of output video: {output_video_size / (1024 * 1024):.2f} MB")
