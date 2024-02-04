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
import shutil
import os

def encode(input_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    shutil.copy(input_file, output_folder)

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
            
            encode(sys.argv[1], sys.argv[2])
        else:
            print("Expected 2 arguemnts (input_file and output_folder), got", len(sys.argv) - 1)
    except:
        print("Error: Invalid arguments. Usage: python encode.py <input_file> <output_folder>")
        sys.exit(1)
