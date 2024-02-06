"""
File: decode.py
Author: Isaac Monheit
Date: 2/4/24
Description: 
            Decompress a BSS compressed image and save it to the output folder.

            Args:
                input_compressed_folder_path (str): Path to the input compressed folder.
                output_folder (str): Path to the output folder.

            Returns:
                str: Path to the decoded folder.
"""

import sys
import cv2
import numpy as np
import os
import subprocess

from is_16_bit import is_16bit_image

def decompress_image(input_compressed_folder_path, output_folder):

    # get both the upper and lower from input folder
    data_files = [f for f in os.listdir(input_compressed_folder_path) if f.endswith('.png')]
    data_files.sort()  # Ensure lower byte file is first

    if len(data_files) != 2:
        print("Error: The input folder should contain exactly two data files.")
        sys.exit(1)

    # create new folder in output folder to hold both decompressed images and copy the pngs to the new folder
    decoded_folder = output_folder
    i = 0
    while os.path.exists(os.path.join(decoded_folder, f'decoded_{i}')):
        i += 1
    decoded_folder = os.path.join(decoded_folder, f'decoded_{i}')
    os.makedirs(decoded_folder, exist_ok=True)
    
    for file in data_files:
        input_file_path = os.path.join(input_compressed_folder_path, file)
        output_file_path = os.path.join(decoded_folder, file.replace('_compressed', ''))

        command = [
            'ffmpeg',
            '-i', input_file_path,
            '-c:v', 'png',
            '-pix_fmt', 'gray',
            '-update', '1',
            output_file_path
        ]
        subprocess.run(command)

    return decoded_folder

def decode(input_folder, output_folder):
 
    decompressed_8bits = decompress_image(input_folder, output_folder)
    print(decompressed_8bits)

    # Get the list of data files in the folder
    data_files = [f for f in os.listdir(decompressed_8bits) if f.endswith('.png')]
    data_files.sort()  # Ensure lower byte file is first

    # Check if there are exactly two data files
    if len(data_files) != 2:
        print("Error: The decompressed input folder should contain exactly two data files.")
        return
    
    # convert the pngs to 8-bit arrays
    lower_byte = cv2.imread(os.path.join(decompressed_8bits, data_files[0]), cv2.IMREAD_UNCHANGED)
    upper_byte = cv2.imread(os.path.join(decompressed_8bits, data_files[1]), cv2.IMREAD_UNCHANGED)

    # print the size of the lower and upper byte files as well as dimensions
    lower_byte_size = os.path.getsize(os.path.join(decompressed_8bits, data_files[0]))
    upper_byte_size = os.path.getsize(os.path.join(decompressed_8bits, data_files[1]))
    print(f"the LSB decompressed size is {lower_byte_size / 1024:.2f} kB")
    print(f"the MSB decompressed size is {upper_byte_size / 1024:.2f} kB")
    
    # Check if the data was successfully read
    if lower_byte is None or upper_byte is None:
        print("Error: Failed to read one or both of the data files.")
        return
        

    # Combine the two 8-bit streams into one 16-bit stream
    height, width = 512, 640
    combined_image = (upper_byte.astype(np.uint16) << 8) | lower_byte.astype(np.uint16)
    
    # Reshape the combined array back to its original image shape
    combined_image = combined_image.reshape((height, width))
    output_file_path = os.path.join(output_folder, 'reconstructed_image.png')
    cv2.imwrite(output_file_path, combined_image)

    if not is_16bit_image(output_file_path):
        print("Error: Output image is not 16-bit depth.")
        sys.exit(1)

    print(f"Reconstructed image saved to {output_file_path}")

    # normalize the image in 8-bit
    img = cv2.imread(output_file_path, cv2.IMREAD_UNCHANGED)
    img_normalized = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    # compare to original image
    img_original = cv2.imread('uncompressed_images/neutrino_capture100.png', cv2.IMREAD_UNCHANGED)
    img_original_normalized = cv2.normalize(img_original, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    # apply CLAHE enhancement to the image
    clahe = cv2.createCLAHE(clipLimit=2000.0, tileGridSize=(16, 12))
    img_enhanced = clahe.apply(img)
    img_enhanced_normalized = cv2.normalize(img_enhanced, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    img_original_enhanced = clahe.apply(img_original)
    img_original_enhanced_normalized = cv2.normalize(img_original_enhanced, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)   

    # cv2.imshow('enhanced Image', clahe.apply(img_original))



    img_size = os.path.getsize(output_file_path)
    img_original_size = os.path.getsize('uncompressed_images/neutrino_capture100.png')
    
    # find the path of both compressed images in the input_folder
    compressed_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    compressed_files.sort()
    compressed_files = [os.path.join(input_folder, f) for f in compressed_files]

    # create variable input_file_size to store the combined size of both the upper and lower byte files in the input_folder
    input_file_size = 0
    for file in compressed_files:
        input_file_size += os.path.getsize(file)
    

    # create a 4 panel image display to compare the original and reconstructed images as well as the CLAHE enhanced images of both adding a space and title for each
    img_display = np.zeros((1024, 1280), dtype=np.uint8)
    img_display[:512, :640] = img_original_normalized
    img_display[:512, 640:] = img_normalized
    img_display[512:, :640] = clahe.apply(img_original_enhanced_normalized)
    img_display[512:, 640:] = img_enhanced_normalized
    cv2.putText(img_display, 'Original Image', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(img_display, 'Reconstructed Image', (650, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(img_display, 'Original Enhanced Image', (10, 540), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(img_display, 'Reconstructed Enhanced Image', (650, 540), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow('Comparison', img_display)

    # IMPORTANT INFORMATION
    print(f'the size of the original image is {img_original_size / 1024:.2f} kB')
    print(f'the size of the reconstructed image is {img_size / 1024:.2f} kB')
    print(f'the size of the input folder is {input_file_size / 1024:.2f} kB')
    difference = cv2.subtract(img, img_original)
    print(f'the percentage of difference between the original and reconstructed images is: {cv2.countNonZero(difference) / (512 * 640) * 100:.2f}%')
    print(f'the compression ratio is: {(img_original_size / input_file_size):.2f}x')
    print("the resultant image is 16-bit" if is_16bit_image(output_file_path) else "the resultant image is not 16-bit")

    cv2.waitKey(0)
    cv2.destroyAllWindows()



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
            
            decode(sys.argv[1], sys.argv[2])
        else:
            print("Expected 2 arguemnts (input_folder and output_folder), got", len(sys.argv) - 1)
    except:
        print("Error: Invalid arguments. Usage: python encode.py <input_folder> <output_folder>")
        sys.exit(1)
