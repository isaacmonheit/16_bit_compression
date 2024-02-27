"""
File: encode.py
Author: Isaac Monheit
Date: 2/4/24
Description: 
            Compress the input file using Bit Stream Splitting (BSS) 
            and save it to the output folder.

            Args:
                input_image_path (str): Path to the input image file.
                output_folder (str): Path to the output folder.

            Usage:
                python3 encode.py <input_image_path> <output_folder>
"""

import sys
import cv2
import os
import numpy as np
import subprocess

from is_16_bit import is_16bit_image

def encode(input_file, output_folder):
    if not is_16bit_image(input_file):
        print("Error: Input file is not 16-bit depth.")
        sys.exit(1)

    image = cv2.imread(input_file, cv2.IMREAD_UNCHANGED) 
    height, width = 512, 640

    # Split 16-bit stream into two 8-bit streams -- something weird is happening here
    upper_byte = (image >> 8).astype(np.uint8)
    lower_byte = (image & 0xFF).astype(np.uint8)

    # Save upper and lower bytes by replacing the .png with _upper.png and _lower.png
    # NOTE THAT THIS ASSUMES THE INPUT FILE IS A .png
    # NEED TO FIX THIS TO WORK WITH OTHER FILE TYPES
    upper_byte_path = os.path.join(output_folder, "MSB", os.path.basename(input_file)[:-4] + "_upper.png")
    lower_byte_path = os.path.join(output_folder, "LSB", os.path.basename(input_file)[:-4] + "_lower.png")

    cv2.imwrite(upper_byte_path, upper_byte.reshape((height, width)))
    cv2.imwrite(lower_byte_path, lower_byte.reshape((height, width)))



def encode_folder(source_folder, target_folder):
    # put all files in the source folder into list to be encoded
    files = [f for f in os.listdir(source_folder) if f.endswith('.png')]
    files.sort()

    # create two folders in target folder to hold the encoded images, one called LSB and the other MSB
    LSB = os.path.join(target_folder, "LSB")
    MSB = os.path.join(target_folder, "MSB")
    os.makedirs(LSB, exist_ok=True)
    os.makedirs(MSB, exist_ok=True)

    for filename in files:
        input_file_path = os.path.join(source_folder, filename)
        if is_16bit_image(input_file_path):
            encode(input_file_path, target_folder)

    # convert LSB and MSB into single YUV videos using FFmpeg
    # -c vvc (after ...d_lower.png) : to use the VVC codec, much slower but insane CR (43x to 266x)
    # data for -c:v vvc is in test3 folders
        
    # most optimal right now, using vvc
    LSB_command = f"ffmpeg -framerate 30 -i {LSB}/neutrino_capture%d_lower.png -c:v vvc -preset 0 -qp 22 {target_folder}/LSB.mp4"
    
    # this one works well but loses a fair bit of quality
    # LSB_command = f"ffmpeg -framerate 30 -i {LSB}/neutrino_capture%d_lower.png -b:v 8M {target_folder}/LSB.mkv"

    # j2k removes metadata, jp2 keeps it
    MSB_command = f"ffmpeg -framerate 30 -i {MSB}/neutrino_capture%d_upper.png -c:v jpeg2000 -format j2k -pred 1 -prog 0 {target_folder}/MSB.mkv"

    # to get info about an encoder, use "ffmpeg -h encoder=encoder_name"

    # havent tried this one yet but should work for H264 lossless
    # MSB_command = f"ffmpeg -framerate 30 -i {MSB}/neutrino_capture%d_upper.png -c:v libx264 -preset veryslow -crf 0 -pix_fmt yuv444p {target_folder}/MSB.mkv"

    # compression ratio of MSB folder to video: 1.18x
    # said to be lossless
    # MSB_command = f"ffmpeg -framerate 30 -i {MSB}/neutrino_capture%d_upper.png -c:v jpeg2000 -pred 1 -q:v 0 {target_folder}/MSB.mkv"
    
    # slow but pretty solid lossy compression
    # MSB_command = f"ffmpeg -framerate 30 -i {MSB}/neutrino_capture%d_upper.png -b:v 20000k -vcodec vvc -vvenc-params InternalBitDepth=8 {target_folder}/MSB.mkv"

    # create a text file that stores LSB and MSB commands
    with open(f"{target_folder}/encode_commands.txt", "w") as f:
        f.write(LSB_command + "\n")
        f.write(MSB_command)

    subprocess.run(LSB_command, shell=True)
    subprocess.run(MSB_command, shell=True)

    # print size of input folder
    input_folder_size = sum(os.path.getsize(f"{source_folder}/{f}") for f in os.listdir(source_folder) if os.path.isfile(f"{source_folder}/{f}"))
    print(f"size of input folder: {input_folder_size / 1024:.2f}kB")

    # print size of LSB folder
    LSB_folder_size = sum(os.path.getsize(f"{LSB}/{f}") for f in os.listdir(LSB) if os.path.isfile(f"{LSB}/{f}"))
    print(f"size of LSB folder: {LSB_folder_size / 1024:.2f}kB")

    LSB_size = os.path.getsize(f"{target_folder}/LSB.mp4")
    print(f"size of LSB.mp4 video: {LSB_size / 1024:.2f}kB") # why is the size so small right now?, total 300 frames = about 60 MB, this video about 1.5 MB

    # print ratio of LSB folder to video
    print(f"compression ratio of LSB folder to video: {LSB_folder_size / LSB_size:.2f}x")


    # do the same for MSB folder and video
    MSB_folder_size = sum(os.path.getsize(f"{MSB}/{f}") for f in os.listdir(MSB) if os.path.isfile(f"{MSB}/{f}"))
    print(f"size of MSB folder: {MSB_folder_size / 1024:.2f}kB")

    MSB_size = os.path.getsize(f"{target_folder}/MSB.mkv")
    print(f"size of MSB.mkv video: {MSB_size / 1024:.2f}kB")

    print(f"compression ratio of MSB folder to video: {MSB_folder_size / MSB_size:.2f}x")


if __name__ == "__main__":
    try:
        if len(sys.argv) == 3:            
            # Check if input file exists
            if not os.path.exists(sys.argv[1]):
                print("Error: Input folder does not exist.")
                sys.exit(1)
            
            # Check if output folder exists
            if not os.path.exists(sys.argv[2]):
                print("Error: Output folder does not exist.")
                sys.exit(1) 

            encode_folder(sys.argv[1], sys.argv[2])
        else:
            print("Expected 2 arguments (input_folder and output_folder), got", len(sys.argv) - 1)
    except:
        print("Error: Something has gone wrong. Usage: python encode.py <input_file> <output_folder>")
        print(sys.exc_info()[0])
        sys.exit(1)

    