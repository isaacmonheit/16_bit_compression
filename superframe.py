import cv2
import numpy as np
import os
from pathlib import Path

def compile_to_superframe(input_folder, output_path):

    frame_paths = [Path(input_folder) / f"neutrino_capture{i}.png" for i in range(300)]
    # frames = []

    # # Check if we found any frames
    # if not frame_paths:
    #     raise ValueError(f"No frames found in the folder {input_folder}.")
    
    # # print number of items in frame_paths
    # print(f"Number of items in frame_paths: {len(frame_paths)}")


    # # Load each image and append to list
    # for frame_path in frame_paths:
    #     print (f"Loading frame: {frame_path}")
    #     frame = cv2.imread(str(frame_path), cv2.IMREAD_UNCHANGED)
    #     if frame is None:
    #         raise ValueError(f"Could not load frame: {frame_path}")
    #     frames.append(frame)

    # if frames[0].dtype != np.uint16:
    #     raise ValueError("The loaded images are not 16-bit.")


    # # Calculate the superframe dimensions
    # frame_height, frame_width = frames[0].shape
    
    # #print the shape of the first frame
    # print(f"Shape of the first frame: {frames[0].shape}")

    # num_frames = len(frames)
    # superframe_width = frame_width * frame_height # each row is the width of all the pixels in a frame added together

    # # Create an empty array for the superframe (height is the number of frames, width is the frame_height * frame_width)
    # superframe = np.zeros((num_frames, superframe_width), dtype=frames[0].dtype)

    # for i, frame in enumerate(frames):
    #     start = 0
    #     for row in range(frame_height):
    #         for j in range(frame_width):
    #             superframe[i][start + j] = frame[row][j]
    #         start = start + frame_width


    # Place each frame in the superframe array
    # for i, frame in enumerate(frames):
    #     start_index = i * frame_width
    #     superframe[:, start_index:start_index + frame_width] = frame

    superframe = cv2.imread(normal_output_path, cv2.IMREAD_UNCHANGED)

    if superframe.dtype != np.uint16:
        raise ValueError("The resultant image is not 16-bit.")
    
    # save the superframe as a png file in the output folder
    cv2.imwrite(normal_output_path, superframe)
    
    # compressing the superframe using jp2
    cv2.imwrite(output_path, superframe, [cv2.IMWRITE_JPEG2000_COMPRESSION_X1000, 50])
    # cv2.imwrite(output_path, superframe, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    # cv2.imwrite(output_path, superframe, [cv2.IMWRITE_WEBP_QUALITY, 100])

    # Save the superframe as an image
    # cv2.imwrite(output_path, superframe)
    print(f"Superframe saved to {output_path}")

    # print the storage size of the superframe in MB
    print(f"Storage size of the superframe: {os.path.getsize(output_path) / (1024 * 1024)} MB")

    # print the compression ratio, size of input folder / size of output superframe
    print(f"Compression ratio: {sum(os.path.getsize(f) for f in frame_paths) / (os.path.getsize(output_path))}")
    
    # print the shape of the superframe
    print(f"Shape of the superframe: {superframe.shape}")

    # display the superframe
    # cv2.imshow('Superframe', superframe)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


# Specify the input folder of 16-bit images and the desired output path for the superframe
input_folder = 'capture'
normal_output_path = 'tests/superframe_tests/superframe.png'
output_path = 'tests/superframe_tests/superframe.jp2'

# Compile the images in the folder into a superframe
compile_to_superframe(input_folder, output_path)


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
    # for i in range(len(frames)):
    #     for j in range(i + 1, len(frames)):
    #         if np.array_equal(frames[i], frames[j]):
    #             raise ValueError(f"Frame {i} and frame {j} are the same.")

    # return each frame to the shape of the original frame dimensions (512, 640)
    for i, frame in enumerate(frames):
        frames[i] = frame.reshape(512, 640)

    # Save each frame to the output folder
    for i, frame in enumerate(frames):
        frame_path = os.path.join(output_folder, f"frame_{i}.png")
        cv2.imwrite(frame_path, frame)
        # print(f"Frame {i} saved to {frame_path}")

    # print the percentage difference between capture/neutrino_capture200.png and frame_200.png
    img = cv2.imread('capture/neutrino_capture200.png', cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread('tests/superframe_tests/split_frames/frame_200.png', cv2.IMREAD_UNCHANGED)
    print(f"Percentage difference between capture/neutrino_capture200.png and frame_200.png: {np.sum(img != img2) / (512 * 640)}")
        

    # display frame 150 in 8 bit
    # clahe = cv2.createCLAHE(clipLimit=2000.0, tileGridSize=(16, 12))
    # img_enhanced = clahe.apply(frames[150])
    # cv2.imshow('Enhanced Frame 150', img_enhanced)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    # BUG FIXING

    #go through all of the folder I have in this directory labeled "capture/" and for each one check it against frames[200], and find the one that is the exact same
    # then print the index of that frame

    # for i in range(0, 299):
    #     img = cv2.imread(f'capture/neutrino_capture{i}.png', cv2.IMREAD_UNCHANGED)
    #     if np.array_equal(img, frames[201]):
    #         print(f"Frame {i} is the same as frame 201")



# Specify the path to the superframe and the desired output folder for the frames
superframe_path = 'tests/superframe_tests/superframe.jp2'
output_folder = 'tests/superframe_tests/split_frames'

# Split the superframe into individual frames
split_superframe(superframe_path, output_folder)



