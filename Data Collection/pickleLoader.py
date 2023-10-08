import numpy as np
import pickle
import cv2

# Colour converter class for colorful topography creation
from colourConverter import ColourConverter

# Constants used for data normalization, set here because min and max function take long times to run
RESOLUTION = (1920, 1080)
MIN_HEIGHT = 601.28766
MAX_HEIGHT = 1770.0
HEIGHT_DIFF = MAX_HEIGHT - MIN_HEIGHT

# Calculated slightly differently, because when examining the difference between two HGT datas we display it using the squared value of the difference
MIN_DIFF = -1123.0024
MAX_DIFF = 345.21582
DIFF_DIFF = MIN_DIFF ** 2

# Normalization for basic DEM creation
def NormalizeValue(value):

    # Handles the -10000s
    if value < 100:
        return -1

    return (value - MIN_HEIGHT) / HEIGHT_DIFF

# Normalization for difference between DEMs
def NormalizeDelta(value):

    # Handles the -10000s
    if value < -1200:
        return -1
    
    return (value ** 2) / DIFF_DIFF

# Normalizes an array with it's given function
def NormalizeArray(arr, norm_func):

    shape = arr.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            arr[i][j] = norm_func(arr[i][j])

# Creates an image for CV2 and uses the data from a normalized array to make it grayscale
def CreateGrayscaleImage(arr):

    shape = arr.shape
    img = np.empty(shape, dtype=np.uint8)
    for i in range(shape[0]):
        for j in range(shape[1]):
            img[i][j] = 255 * arr[i][j]

    return img

# Loads in numpy pickles from byteReader
with open("glacier_1.pickle", 'rb') as file:
    glacier_1 = pickle.load(file)

with open("glacier_2.pickle", 'rb') as file:
    glacier_2 = pickle.load(file)

with open("glacier_diff.pickle", 'rb') as file:
    glacier_diff = pickle.load(file)

# Finds the proper size to make the images so they are a reasonable size to display with CV2
resize_shape = list(glacier_1.shape)
scale_factor = 1

while resize_shape[0] > (RESOLUTION[0] * 0.5) or resize_shape[1] > (RESOLUTION[1] * 0.5):
    resize_shape[0] /= 2
    resize_shape[1] /= 2
    scale_factor /= 2

glacier_1 = cv2.resize(glacier_1, None, fx=scale_factor, fy=scale_factor)
glacier_2 = cv2.resize(glacier_2, None, fx=scale_factor, fy=scale_factor)
glacier_diff = cv2.resize(glacier_diff, None, fx=scale_factor, fy=scale_factor)

# Normalizes all the data
NormalizeArray(glacier_1, NormalizeValue)
NormalizeArray(glacier_2, NormalizeValue)
NormalizeArray(glacier_diff, NormalizeDelta)

# Creates grayscale images
img_1 = CreateGrayscaleImage(glacier_1)
img_2 = CreateGrayscaleImage(glacier_2)
img_3 = CreateGrayscaleImage(glacier_diff)

# Uses colour converter class to create colorful DEM
color_converter = ColourConverter()

color_img_1 = color_converter.colour_function(glacier_1)
color_img_2 = color_converter.colour_function(glacier_2)
color_img_3 = color_converter.colour_function(glacier_diff)

# Saves and displays all the images
cv2.imwrite("Glacier_1.png", img_1)
cv2.imwrite("Glacier_2.png", img_2)
cv2.imwrite("Glacier_diff.png", img_3)

cv2.imshow("Glacier 1", img_1)
cv2.imshow("Glacier 2", img_2)
cv2.imshow("Glacier diff", img_3)

cv2.imwrite("Glacier_1_colored.png", color_img_1)
cv2.imwrite("Glacier_2_colored.png", color_img_2)
cv2.imwrite("Glacier_diff_colored.png", color_img_3)

cv2.imshow("Glacier 1 colored", color_img_1)
cv2.imshow("Glacier 2 colored", color_img_2)
cv2.imshow("Glacier diff colored", color_img_3)
cv2.waitKey(0)