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

def compress_image(input_image_path, output_folder, compression_ratio=10):
    # Calculate target bitrate based on desired compression ratio and input image size
    input_image_size = os.path.getsize(input_image_path)
    target_bitrate = (input_image_size * 8 / compression_ratio) / 1000  # Convert to kilobits
    print(f"Target bitrate: {target_bitrate} kbps")

    # Construct the output file path
    output_file_path = os.path.join(output_folder, os.path.basename(input_image_path)[:-4] + "_compressed.png")

    """ Goal for a basic FFmpeg command:  ffmpeg -i <input> -c:v vvc -b:v 2600k -preset faster <output> """

    # Construct FFmpeg command for compression
    command = [
        'ffmpeg',
        '-i', input_image_path,
        '-c:v', 'vvc',
        '-b:v', f'{target_bitrate}k',
        '-preset', 'faster',
        '-update', '1',
        output_file_path
    ]

    subprocess.run(command)
    os.remove(input_image_path)
    return output_file_path



def encode(input_file, output_folder):
    if not is_16bit_image(input_file):
        print("Error: Input file is not 16-bit depth.")
        sys.exit(1)

    #print size of input file
    input_file_size = os.path.getsize(input_file)

    image = cv2.imread(input_file, cv2.IMREAD_UNCHANGED) 
    height, width = 512, 640

    # Split 16-bit stream into two 8-bit streams
    upper_byte = (image >> 8).astype(np.uint8)
    lower_byte = (image & 0xFF).astype(np.uint8)

    # Create a new folder for encoded images
    encoded_folder = output_folder
    i = 0
    while os.path.exists(os.path.join(encoded_folder, f"encoded_{i}")):
        i += 1
    encoded_folder = os.path.join(encoded_folder, f"encoded_{i}")
    os.makedirs(encoded_folder)

    # Save upper and lower bytes by replacing the .png with _upper.png and _lower.png
    # NOTE THAT THIS ASSUMES THE INPUT FILE IS A .png
    # NEED TO FIX THIS TO WORK WITH OTHER FILE TYPES
    upper_byte_path = os.path.join(encoded_folder, os.path.basename(input_file)[:-4] + "_upper.png")
    lower_byte_path = os.path.join(encoded_folder, os.path.basename(input_file)[:-4] + "_lower.png")

    cv2.imwrite(upper_byte_path, upper_byte.reshape((height, width)))
    cv2.imwrite(lower_byte_path, lower_byte.reshape((height, width)))

    compressed_upper_byte_path = compress_image(upper_byte_path, encoded_folder)
    compressed_lower_byte_path = compress_image(lower_byte_path, encoded_folder)



    # print what folder the compressed images are in
    print("The compressed images are in", encoded_folder)

    #print size of compressed files
    compressed_upper_byte_size = os.path.getsize(compressed_upper_byte_path)
    compressed_lower_byte_size = os.path.getsize(compressed_lower_byte_path)
    print(f"the LSB compressed size is {compressed_lower_byte_size / 1024:.2f} kB")
    print(f"the MSB compressed size is {compressed_upper_byte_size / 1024:.2f} kB")

    #print size of input file and compression ratio for both files combined
    compressed_file_size = compressed_upper_byte_size + compressed_lower_byte_size
    print(f"the total compressed file size is {compressed_file_size / 1024:.2f} kB")
    print(f"the compression ratio is {(input_file_size / compressed_file_size):.2f}x")

if __name__ == "__main__":
    try:
        if len(sys.argv) == 3:            
            # Check if input file exists
            if not os.path.isfile(sys.argv[1]):
                print("Error: Input file does not exist.")
                sys.exit(1)
            
            # Check if output folder exists
            if not os.path.exists(sys.argv[2]):
                print("Error: Output folder does not exist.")
                sys.exit(1) 
        else:
            print("Expected 2 arguments (input_file and output_folder), got", len(sys.argv) - 1)
    except:
        print("Error: Invalid arguments. Usage: python encode.py <input_file> <output_folder>")
        sys.exit(1)

    encode(sys.argv[1], sys.argv[2])