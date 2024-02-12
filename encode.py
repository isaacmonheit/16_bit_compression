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
from image_display_8bit import display_8_bit_images


#DONT THINK I NEED THIS AT ALL ACTUALLY
# def compress_image(input_image_path, output_folder, compression_ratio=10):
#     # Calculate target bitrate based on desired compression ratio and input image size
#     input_image_size = os.path.getsize(input_image_path)
#     target_bitrate = (input_image_size * 8 / compression_ratio) / 1000  # Convert to kilobits
#     print(f"Target bitrate: {target_bitrate} kbps")

#     # Construct the output file path
#     output_file_path = os.path.join(output_folder, os.path.basename(input_image_path)[:-10] + "_compressed.png")

#     """ Goal for a basic FFmpeg command:  ffmpeg -i <input> -c:v vvc -b:v 2600k -preset faster <output> """

#     # Construct FFmpeg command for compression
#     command = [
#         'ffmpeg',
#         '-i', input_image_path,
#         '-c:v', 'vvc',
#         '-b:v', f'{target_bitrate}k',
#         '-preset', 'faster',
#         '-update', '1',
#         output_file_path
#     ]

#     subprocess.run(command)
#     os.remove(input_image_path)
#     return output_file_path



def encode(input_file, output_folder):
    if not is_16bit_image(input_file):
        print("Error: Input file is not 16-bit depth.")
        sys.exit(1)

    #print size of input file
    input_file_size = os.path.getsize(input_file)

    image = cv2.imread(input_file, cv2.IMREAD_UNCHANGED) 
    height, width = 512, 640

    # Split 16-bit stream into two 8-bit streams -- something weird is happening here
    upper_byte = (image >> 8).astype(np.uint8)
    lower_byte = (image & 0xFF).astype(np.uint8)

    # Create a new folder for encoded images
    # encoded_folder = output_folder
    # i = 0
    # while os.path.exists(os.path.join(encoded_folder, f"encoded_{i}")):
    #     i += 1
    # encoded_folder = os.path.join(encoded_folder, f"encoded_{i}")
    # os.makedirs(encoded_folder)

    # Save upper and lower bytes by replacing the .png with _upper.png and _lower.png
    # NOTE THAT THIS ASSUMES THE INPUT FILE IS A .png
    # NEED TO FIX THIS TO WORK WITH OTHER FILE TYPES
    upper_byte_path = os.path.join(output_folder, "MSB", os.path.basename(input_file)[:-4] + "_upper.png")
    lower_byte_path = os.path.join(output_folder, "LSB", os.path.basename(input_file)[:-4] + "_lower.png")

    cv2.imwrite(upper_byte_path, upper_byte.reshape((height, width)))
    cv2.imwrite(lower_byte_path, lower_byte.reshape((height, width)))






    # print what folder the compressed images are in
    # print("The compressed images are in", output_folder)

    # print size of compressed files
    # compressed_upper_byte_size = os.path.getsize(compressed_upper_byte_path)
    # compressed_lower_byte_size = os.path.getsize(compressed_lower_byte_path)
    # print(f"the LSB compressed size is {compressed_lower_byte_size / 1024:.2f} kB")
    # print(f"the MSB compressed size is {compressed_upper_byte_size / 1024:.2f} kB")

    #print size of input file and compression ratio for both files combined
    # compressed_file_size = compressed_upper_byte_size + compressed_lower_byte_size
    # print(f"the total compressed file size is {compressed_file_size / 1024:.2f} kB")
    # print(f"the compression ratio is {(input_file_size / compressed_file_size):.2f}x")


def encode_folder(source_folder, target_folder):
    # put all files in the source folder into list to be encoded
    files = [f for f in os.listdir(source_folder) if f.endswith('.png')]
    files.sort()

    # create two folders in target folder to hold the encoded images, one called LSB and the other MSB
    LSB = os.path.join(target_folder, "LSB")
    MSB = os.path.join(target_folder, "MSB")
    os.makedirs(LSB, exist_ok=True)
    os.makedirs(MSB, exist_ok=True)

    # for filename in files:
    #     input_file_path = os.path.join(source_folder, filename)
    #     if is_16bit_image(input_file_path):
    #         encode(input_file_path, target_folder)

    # convert LSB and MSB into single YUV videos using FFmpeg
    # -c vvc : to use the VVC codec, much slower but insane CR (43x to 266x)
    LSB_command = f"ffmpeg -framerate 30 -i {LSB}/neutrino_capture%d_lower.png {target_folder}/LSB.mp4"
    MSB_command = f"ffmpeg -framerate 30 -i {MSB}/neutrino_capture%d_upper.png {target_folder}/MSB.mp4"

    subprocess.run(LSB_command, shell=True)
    subprocess.run(MSB_command, shell=True)

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

    MSB_size = os.path.getsize(f"{target_folder}/MSB.mp4")
    print(f"size of MSB.mp4 video: {MSB_size / 1024:.2f}kB")

    print(f"compression ratio of MSB folder to video: {MSB_folder_size / MSB_size:.2f}x")






    # run compress_image on LSB and MSB
    # compressed_upper_byte_path = compress_image(MSB, target_folder)
    # compressed_lower_byte_path = compress_image(LSB, target_folder)

    # compressed_upper_byte_path = compress_image(upper_byte_path, encoded_folder)
    # compressed_lower_byte_path = compress_image(lower_byte_path, encoded_folder)


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

    