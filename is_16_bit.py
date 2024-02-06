"""
File: is_16_bit.py
Author: Isaac Monheit
Date: 1/30/24
Description: Checks whether given image has 16-bit depth or not
"""
import cv2

def is_16bit_image(image_path):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        return img.dtype == 'uint16'
    except Exception as e:
        print(f"Error: {e}")
        return False

# Example usage:
if __name__ == "__main__":
    image_path = 'compressed_images/neutrino_capture100.png'
    result = is_16bit_image(image_path)
    yes_or_no = "Indeed" if result else "Nah"
    print(f"Is {image_path} a 16-bit image? {yes_or_no}")
