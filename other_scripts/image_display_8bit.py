import numpy as np
import cv2
import os

def display_8_bit_images(folder_path, image_shape):
    # Get the list of raw data files in the folder
    image_files = [f for f in os.listdir(folder_path)]

    # Check if there are exactly two image files
    if len(image_files) != 2:
        print("Error: The folder should contain exactly two image files.")
        return

    # Read the images as raw data and reshape
    lower = np.fromfile(os.path.join(folder_path, image_files[0]), dtype=np.uint8).reshape(image_shape)
    upper = np.fromfile(os.path.join(folder_path, image_files[1]), dtype=np.uint8).reshape(image_shape)

    #check size of the images as total space used up by the images
    print("Size of lower image: ", lower.size)
    print("Size of upper image: ", upper.size)

    # Check if the images were successfully read
    if lower is None or upper is None:
        print("Error: Failed to read one or both of the images.")
        return

    # Display the images
    cv2.imshow('lower bytes (LSB)', lower)
    cv2.imshow('upper bytes (MSB)', upper)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
# display_8_bit_images('path/to/folder', (512, 640))  # Replace with your image's dimensions
