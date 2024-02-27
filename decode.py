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

def decode_video (input_folder, output_folder):

    # get the list of video files in the input folder if it ends with mp4 or mkv
    video_files = [f for f in os.listdir(input_folder) if f.endswith('.mkv') or f.endswith('.mp4')]

    # for each video split it into 8-bit frames and save them to {output_folder}/{video_name}
    for file in video_files:
        input_file_path = os.path.join(input_folder, file)
        output_file_path = os.path.join(output_folder, file[:-4])
        os.makedirs(output_file_path, exist_ok=True)

        command = [
            'ffmpeg',
            '-i', input_file_path,
            '-c:v', 'png',
            '-pix_fmt', 'gray',
            os.path.join(output_file_path, 'frame_%d.png')
        ]
        subprocess.run(command)
    
    # get the number of files in LSB folder
    output_file_path = os.path.join(output_folder, 'LSB')
    num_files = len([f for f in os.listdir(output_file_path) if f.endswith('.png')])

    os.makedirs(os.path.join(output_folder, 'reconstructed_images'), exist_ok=True)

    # take each frame in both folders and combine them into a 16-bit image and save it to {output_folder}/{video_name}
    for i in range(1, num_files + 1):
        # loop through all the files in output_folder/LSB and output_folder/MSB and combine them into a 16-bit image starting with frame_1.png
        lower_byte = cv2.imread(os.path.join(output_folder, 'LSB', f'frame_{i}.png'), cv2.IMREAD_UNCHANGED)
        upper_byte = cv2.imread(os.path.join(output_folder, 'MSB', f'frame_{i}.png'), cv2.IMREAD_UNCHANGED)

        # combine the two 8-bit streams into one 16-bit stream
        height, width = 512, 640
        combined_image = (upper_byte.astype(np.uint16) << 8) | lower_byte.astype(np.uint16)

        # reshape the combined array back to its original image shape and place in new folder within output_folder called "reconstructed_images"
        combined_image = combined_image.reshape((height, width))
        output_file_path = os.path.join(output_folder, 'reconstructed_images', f'reconstructed_frame_{i}.png')
        cv2.imwrite(output_file_path, combined_image)


    #compare the reconstructed images to the original images
    pic_num = int(input("Enter the number of the picture you would like to compare (1-300): "))
    for i in range(pic_num, pic_num + 1):
        # load the original image and the reconstructed image
        img = cv2.imread(os.path.join(output_folder, 'reconstructed_images', f'reconstructed_frame_{i}.png'), cv2.IMREAD_UNCHANGED)
        img_original = cv2.imread(f'capture/neutrino_capture{i - 1}.png', cv2.IMREAD_UNCHANGED)

        # normalize the images
        img_normalized = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        img_original_normalized = cv2.normalize(img_original, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

        # apply CLAHE enhancement to the images
        clahe = cv2.createCLAHE(clipLimit=2000.0, tileGridSize=(16, 12))
        img_enhanced = clahe.apply(img)
        img_enhanced_normalized = cv2.normalize(img_enhanced, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

        img_original_enhanced = clahe.apply(img_original)
        img_original_enhanced_normalized = cv2.normalize(img_original_enhanced, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)   

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

        print(f"\nComplete video information ({input_folder}/{output_folder}):\n")

        # print the command used to compress the video from input_folder/encode_commands.txt line by line with a space between each
        with open(f"{input_folder}/encode_commands.txt", "r") as file:
            # print("\tthe command used to compress the video is:")
            for line in file:
                print(f"\t{line}", end="")

        print("\n")

        # IMPORTANT INFORMATION -------------------------------------------------
        # print the size of the folder named "capture"
        og_folder_size = sum(os.path.getsize(f"capture/{f}") for f in os.listdir("capture") if os.path.isfile(f"capture/{f}"))
        print(f"\tsize of capture folder (pre compression): {og_folder_size / 1024:.2f}kB")

        # print the size of the input folder
        input_folder_size = sum(os.path.getsize(f"{input_folder}/{f}") for f in os.listdir(input_folder) if os.path.isfile(f"{input_folder}/{f}"))
        print(f"\tsize of input folder (post compression): {input_folder_size / 1024:.2f}kB")

        # CR = original size / compressed size
        print(f"\tcompression ratio: {og_folder_size / input_folder_size:.2f}x")

        # print the size of all elements in the output_folder
        reconstructed_images_size = 0
        for file in os.listdir(os.path.join(output_folder, 'reconstructed_images')):
            reconstructed_images_size += os.path.getsize(os.path.join(output_folder, 'reconstructed_images', file))
        print(f"\tsize of recontructed images (post decompression) {reconstructed_images_size / 1024:.2f} kB")


        print("\n-----------------------------------------------------------------------------------------------\n")
        print("Single image information (neutrino_capture250.png) before and after:\n")
        print(f'\tthe size of the original image is {os.path.getsize(f"capture/neutrino_capture{i - 1}.png") / 1024:.2f} kB')
        print(f'\tthe size of the reconstructed image is {os.path.getsize(os.path.join(output_folder, "reconstructed_images", f"reconstructed_frame_{i}.png")) / 1024:.2f} kB')
        print(f'\tthe percentage of difference between the original and reconstructed images is: {cv2.countNonZero(cv2.subtract(img, img_original)) / (512 * 640) * 100:.2f}%')
        # print("\tthe resultant image is 16-bit" if is_16bit_image(os.path.join(output_folder, "reconstructed_images", f"reconstructed_frame_{i}.png")) else "the resultant image is not 16-bit")
        # print("\n")

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
            
            decode_video(sys.argv[1], sys.argv[2])
        else:
            print("Expected 2 arguemnts (input_folder and output_folder), got", len(sys.argv) - 1)
    except:
        print("Error: Something has gone wrong. Usage: python encode.py <input_folder> <output_folder>")
        print(sys.exc_info())
        sys.exit(1)
