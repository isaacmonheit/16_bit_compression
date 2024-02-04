"""
File: VVenC_script.py
Author: Isaac Monheit
Date: 1/30/24
Description: Simple script for running the expert mode encoder (vvencFFapp) in order 
             to have 16-bit depth and keep the correct settings

             Right now -- works with vvencapp but not vvencFFapp because of the way im
             running cmake to initially build the project, not sure what I need to change
             I'm trying to figure it out
"""
import subprocess

# Define your variables
preset = "medium"
input_file = "capture/neutrino_capture100.png"
resolution = "640x512"
frame_rate = 15
target_bitrate = 1000000
num_passes = 2
qpa = 1
threads = -1
input_bit_depth = 16
internal_bit_depth = 16
output_file = "compressed_images/neutrino_capture100_compressed_test1.266"

# Construct the command
command = [
    'vvencFFapp',
    '--preset', preset,
    '--InputFile', input_file,
    '-s', resolution,
    '-fr', str(frame_rate),
    '-TargetBitrate', str(target_bitrate),
    '--NumPasses', str(num_passes),
    '-qpa', str(qpa),
    '-t', str(threads),
    "--InputBitDepth", str(input_bit_depth),
    "--InternalBitDepth", str(internal_bit_depth),
    '-b', output_file
]

# Run the command
subprocess.run(command)
