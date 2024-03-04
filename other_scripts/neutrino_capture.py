import cv2
import time

file_prefix = "capture/neutrino_capture"
file_ext = ".png"

cap = cv2.VideoCapture("/dev/video4")  # Use 0 for the default camera, change if necessary

# Set the desired frame width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Adjust the width as needed
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)  # Adjust the height as needed
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Check if the camera supports 16-bit depth (bit depth may vary)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', '1', '6', ' ')) 
cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)

num_frames = 300
frame_interval_ms = 1000.0 / 30.0

mark = time.perf_counter()
for i in range(num_frames):
    print("Capturing dual images...")
    ret, frame = cap.read()

    filename = file_prefix + str(i) + file_ext  # Change the filename as needed
    result = cv2.imwrite(filename, frame)
    delta = time.perf_counter() - mark
    mark = time.perf_counter()
    time.sleep((frame_interval_ms - delta) / 1000.0)
