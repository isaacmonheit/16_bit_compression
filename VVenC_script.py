"""
File: VVenC_script.py
Author: Isaac Monheit
Date: 1/30/24
Description: Simple script for running the expert mode encoder (vvencFFapp) in order 
             to have 16-bit depth and keep the correct settings

             Right now -- works with vvencapp but not vvencFFapp because of the way im
             running cmake to initially build the project, not sure what I need to change
             I'm trying to figure it out

             Working solution to downloading vvencFFapp and running it in the terminal
                'sudo make install-ffapp=1 install-release install-prefix=/usr/local'
             """
import subprocess

# Define your variables
preset = "medium"
input_file = "capture"
resolution = "640x512"
frame_rate = 30
target_bitrate = 1000000
num_passes = 2
qpa = 1
threads = -1
input_bit_depth = 16
# internal_bit_depth = 16
output_file = "neutrino_capture100_compressed_test1.266"

# Construct the command
# command = [
#     'vvencFFapp',
#     '--preset', preset,
#     '--InputFile', input_file,
#     '-s', resolution,
#     '-fr', str(frame_rate),
#     '--TargetBitrate', str(target_bitrate),
#     '--NumPasses', str(num_passes),
#     '-qpa', str(qpa),
#     '-t', str(threads),
#     "--InputBitDepth", str(input_bit_depth),
#     '-b', output_file
# ]

# command = f"vvencFFapp --preset {preset} --InputFile {input_file} -s {resolution} -fr {frame_rate} --TargetBitrate {target_bitrate} --NumPasses {num_passes} -qpa {qpa} -t {threads} --InputBitDepth {input_bit_depth} -b {output_file}"
command0 = f"ffmpeg -framerate 30 -i capture/neutrino_capture%d.png -c:v rawvideo -pix_fmt yuv420p 8bit_output_video.yuv"

command = f"vvencFFapp -i 8bit_output_video.yuv --InputChromaFormat 400 -s {resolution} -fr {frame_rate} --preset medium -b {output_file}"

# print length (in seconds) of 8bit_output_video.yuv
command1 = f"ffprobe -i 8bit_output_video.yuv -show_entries format=duration -v quiet -of csv=\"p=0\""
subprocess.run(command1, shell=True)

# Run the command
# subprocess.run(command0, shell=True)
# subprocess.run(command, shell=True)

# print size of input and output files
import os
input_size = os.path.getsize(input_file)
output_size = os.path.getsize(output_file)
print(f"Input file size: {input_size} bytes")
print(f"Output file size: {output_size} bytes")
