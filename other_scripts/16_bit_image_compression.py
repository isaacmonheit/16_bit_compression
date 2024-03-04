"""
File: 16_bit_image_compression.py
Author: Isaac Monheit
Date: 1/29/24
Description: Takes in a 16-bit image and compresses it using the openCV png/jpeg compresion,
             then prints out some info about the size of both the old and new image

             NOT HELPFUL AT ALL, THE OPENCV COMPRESSION NOT GOOD
"""

import cv2
import os
import numpy as np

def check_bit_depth(image):
    """Check if the image is 16-bit."""
    return image.dtype == np.uint16

def compress_image(input_image_path, output_image_path, compression_params):
    """Compress the image and save it to the output path."""
    # Read the image
    image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)
    
    # Check if the image is 16-bit
    if not check_bit_depth(image):
        print("The image is not 16-bit.")
        return
    
    # Compress and save the image
    cv2.imwrite(output_image_path, image, compression_params)
    
    # Calculate the file sizes and compression ratio
    original_size = os.path.getsize(input_image_path)
    compressed_size = os.path.getsize(output_image_path)
    compression_ratio = original_size / compressed_size
    
    print(f"Original Size: {original_size} bytes")
    print(f"Compressed Size: {compressed_size} bytes")
    print(f"Compression Ratio: {compression_ratio:.2f}")

# Specify your paths and parameters
input_image_path = 'capture/neutrino_capture200.png'
output_folder = 'compressed_images'
output_image_path = os.path.join(output_folder, 'neutrino_capture200_compressed.png')

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True) 

# options are "cv2.IMWRITE_JPEG_QUALITY" and "cv2.IMWRITE_PNG_COMPRESSION"
compression_type = cv2.IMWRITE_PNG_COMPRESSION

# Specify compression format and parameters
# For PNG, compression range is 0 (no compression) to 9 (max compression)
# For JPEG, compression range is 0-100, lower means more compression
compression_params = [int(compression_type), 9]

compress_image(input_image_path, output_image_path, compression_params)
