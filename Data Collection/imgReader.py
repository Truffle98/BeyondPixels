import numpy as np
import cv2
import pickle

# File to get small parts of the png, very fine tuned for specific pictures
# Most of these functions and arrays come from other files, this is just a makeshift file for curated purposes
RESOLUTION = (1920, 1080)
MIN_HEIGHT = 601.28766
MAX_HEIGHT = 1770.0
HEIGHT_DIFF = MAX_HEIGHT - MIN_HEIGHT

MIN_DIFF = -1123.0024
MAX_DIFF = 345.21582
DIFF_DIFF = MIN_DIFF ** 2

# Normalize functions
def NormalizeValue(value):

    if value < 100:
        return 0

    return (value - MIN_HEIGHT) / HEIGHT_DIFF

def NormalizeDelta(value):

    if value < -1200:
        return 0
    
    return (value ** 2) / DIFF_DIFF

# Open pickles
with open("glacier_1.pickle", 'rb') as file:
    glacier_1 = pickle.load(file)

with open("glacier_2.pickle", 'rb') as file:
    glacier_2 = pickle.load(file)

with open("glacier_diff.pickle", 'rb') as file:
    glacier_diff = pickle.load(file)

# This is used for viewing the image before making it smaller if needed 
resize_shape = list(glacier_1.shape)
scale_factor = 1
while resize_shape[0] > (RESOLUTION[0] * 0.5) or resize_shape[1] > (RESOLUTION[1] * 0.5):
    resize_shape[0] /= 2
    resize_shape[1] /= 2
    scale_factor /= 2

glacier_1 = cv2.resize(glacier_1, None, fx=scale_factor, fy=scale_factor)
glacier_2 = cv2.resize(glacier_2, None, fx=scale_factor, fy=scale_factor)
glacier_diff = cv2.resize(glacier_diff, None, fx=scale_factor, fy=scale_factor)

# Fine tune the location of the image to take a section of
shape = glacier_1.shape
start = (int(160), int(225))
size = (160, 160)

# Gets a smaller part of each image, over the exact same part
glacier_1 = glacier_1[start[0]:start[0] + size[0], start[1]:start[1] + size[1]]
glacier_2 = glacier_2[start[0]:start[0] + size[0], start[1]:start[1] + size[1]]
glacier_diff = glacier_diff[start[0]:start[0] + size[0], start[1]:start[1] + size[1]]

# Prepares images to be saved
img_1 = np.empty((glacier_diff.shape[0], glacier_diff.shape[1]), dtype=np.uint8)
img_2 = np.empty((glacier_diff.shape[0], glacier_diff.shape[1]), dtype=np.uint8)
img_3 = np.empty((glacier_diff.shape[0], glacier_diff.shape[1]), dtype=np.uint8)

# Creates grayscale images
for i in range(glacier_diff.shape[0]):
    for j in range(glacier_diff.shape[1]):

        img_1[i][j] = 255 * NormalizeValue(glacier_1[i][j])
        img_2[i][j] = 255 * NormalizeValue(glacier_2[i][j])
        img_3[i][j] = 255 * NormalizeDelta(glacier_diff[i][j])

# Saves as pickles and pngs
with open("glacier_1_export.pickle", 'wb') as file:
    pickle.dump(img_1, file)

with open("glacier_2_export.pickle", 'wb') as file:
    pickle.dump(img_2, file)

with open("glacier_diff_export.pickle", 'wb') as file:
    pickle.dump(img_3, file)

cv2.imwrite("Glacier_1_small.png", img_1)
cv2.imwrite("Glacier_2_small.png", img_2)
cv2.imwrite("Glacier_diff_small.png", img_3)