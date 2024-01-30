import cv2

# Read 16-bit grayscale PNG image
img = cv2.imread('capture/neutrino_capture200.png', cv2.IMREAD_UNCHANGED)

# Normalize the image to 8-bits
img_normalized = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

# Apply CLAHE enhancement to the image
clahe = cv2.createCLAHE(clipLimit=2000.0, tileGridSize=(16, 12))
img_enhanced = clahe.apply(img)

# Display the normalized image
cv2.imshow('Normalized Image', img_normalized)

# Display the image with CLAHE enhancement
cv2.imshow('Enhanced Image', img_enhanced)

cv2.waitKey(0)
cv2.destroyAllWindows()
