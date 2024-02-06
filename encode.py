"""
File: encode.py
Author: Isaac Monheit
Date: 2/4/24
Description: 
            Encode the input file and save the encoded content to the output folder.

            Args:
                input_file (str): Path to the input file.
                output_folder (str): Path to the output folder.

            Usage:
                python3 encode.py <input_file> <output_folder>
"""

import sys
import cv2
import os
import numpy as np

from is_16_bit import is_16bit_image
from image_display_8bit import display_8_bit_images

def encode(input_file, output_folder):
    if not is_16bit_image(input_file):
        print("Error: Input file is not 16-bit depth.")
        sys.exit(1)

    image = cv2.imread(input_file, cv2.IMREAD_UNCHANGED) 

    height, width = 512, 640

    # Split 16-bit stream into two 8-bit streams
    upper_byte = (image >> 8).astype(np.uint8)
    lower_byte = (image & 0xFF).astype(np.uint8)

    # # Normalize the images to 8-bits
    # upper_byte = cv2.normalize(upper_byte, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    # lower_byte = cv2.normalize(lower_byte, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    # Create a new folder for encoded images
    encoded_folder = output_folder
    i = 1
    while os.path.exists(os.path.join(encoded_folder, f"encoded_{i}")):
        i += 1
    encoded_folder = os.path.join(encoded_folder, f"encoded_{i}")
    os.makedirs(encoded_folder)

    # Save upper byte as 8-bit array
    upper_byte_path = os.path.join(encoded_folder, f"{os.path.basename(input_file)}_upper.png")
    upper_byte.tofile(upper_byte_path)

    # Save lower byte as 8-bit array
    lower_byte_path = os.path.join(encoded_folder, f"{os.path.basename(input_file)}_lower.png")
    lower_byte.tofile(lower_byte_path)

    # test and view both images
    display_8_bit_images(encoded_folder, (height, width))


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