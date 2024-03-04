import cv2
import numpy as np
import os
from pathlib import Path

def compile_to_superframe(input_folder, output_path):
    # store all file paths in input_folder into a list called frame_paths
    frame_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.png')]
    frames = []

    # Check if we found any frames
    if not frame_paths:
        raise ValueError(f"No frames found in the folder {input_folder}.")
    
    # print number of items in frame_paths
    print(f"Number of items in frame_paths: {len(frame_paths)}")


    # Load each image and append to list
    for frame_path in frame_paths:
        frame = cv2.imread(str(frame_path), cv2.IMREAD_UNCHANGED)
        if frame is None:
            raise ValueError(f"Could not load frame: {frame_path}")
        frames.append(frame)

    if frames[0].dtype != np.uint16:
        raise ValueError("The loaded images are not 16-bit.")


    # Calculate the superframe dimensions
    frame_height, frame_width = frames[0].shape
    
    #print the shape of the first frame
    print(f"Shape of the first frame: {frames[0].shape}")

    num_frames = len(frames)
    superframe_width = frame_width * frame_height # each row is the width of all the pixels in a frame added together

    # Create an empty array for the superframe (height is the number of frames, width is the frame_height * frame_width)
    superframe = np.zeros((num_frames, superframe_width), dtype=frames[0].dtype)

    for i, frame in enumerate(frames):
        start = 0
        for row in range(frame_height):
            for j in range(frame_width):
                superframe[i][start + j] = frame[row][j]
            start = start + frame_width

    # Place each frame in the superframe array
    # for i, frame in enumerate(frames):
    #     start_index = i * frame_width
    #     superframe[:, start_index:start_index + frame_width] = frame

    if superframe.dtype != np.uint16:
        raise ValueError("The resultant image is not 16-bit.")

    # Save the superframe as an image
    cv2.imwrite(output_path, superframe)
    print(f"Superframe saved to {output_path}")

    # display the superframe
    cv2.imshow('Superframe', superframe)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Specify the input folder of 16-bit images and the desired output path for the superframe
input_folder = 'capture'
output_path = 'tests/superframe_tests/superframe.png'

# Compile the images in the folder into a superframe
# compile_to_superframe(input_folder, output_path)


# create a function that takes in a superframe and splits it into frames

def split_superframe(superframe_path, output_folder):
    # Load the superframe
    superframe = cv2.imread(superframe_path, cv2.IMREAD_UNCHANGED)

    # Check if the superframe was loaded
    if superframe is None:
        raise ValueError(f"Could not load superframe: {superframe_path}")

    # Check if the superframe is 16-bit
    if superframe.dtype != np.uint16:
        raise ValueError("The loaded image is not 16-bit.")

    # Get the number of frames and the dimensions of each frame
    num_frames, superframe_width = superframe.shape

    frame_height = superframe_width // superframe_width

    # Split the superframe into individual frames
    frames = np.split(superframe, num_frames, axis=0)

    # make sure the frames are all different from each other
    for i in range(len(frames)):
        for j in range(i + 1, len(frames)):
            if np.array_equal(frames[i], frames[j]):
                raise ValueError(f"Frame {i} and frame {j} are the same.")

    # return each frame to the shape of the original frame dimensions (512, 640)
    for i, frame in enumerate(frames):
        frames[i] = frame.reshape((512, 640))

    # Save each frame to the output folder
    for i, frame in enumerate(frames):
        frame_path = os.path.join(output_folder, f"frame_{i}.png")
        cv2.imwrite(frame_path, frame)
        print(f"Frame {i} saved to {frame_path}")

# Specify the path to the superframe and the desired output folder for the frames
superframe_path = 'tests/superframe_tests/superframe.png'
output_folder = 'tests/superframe_tests/split_frames'

# Split the superframe into individual frames
split_superframe(superframe_path, output_folder)