import numpy as np
import struct
import time
import cv2
import pickle

"""
This file reads in bytes from HGT files and executes functions to properly read in the data and make the two HGT files comparable to eachother
This is done by lining them up and resampling the data to create identical pixel resolutions, then running lots of diagnostic functions to get info
"""

# These constants are setup for inputs from the metadata of the SAR data
DATA_SHAPE_1 = (12513, 8672)
DATA_SHAPE_2 = (12537, 8677)

START_LOC_1 = (65.094873840000005, -19.093142400000001)
START_LOC_2 = (65.08831776000001, -19.09880901)

POINT_SCALE_1 = (-5.5560000000000003e-05, 0.00011111)
POINT_SCALE_2 = (-5.556e-05, 0.00011111)

# Time for optimization purposes
start_time = time.time()

# This class holds lots of information about a HGT file, as well as a member function to read it in from a path
class HGTData():

    # Needs to be initialized with a path to the HGT file, the shape of the data, 
    #   the start location in lat and long, and the scale of each point in degrees
    def __init__(self, path, shape, start_loc, point_scale):

        self.shape = shape
        self.point_scale = point_scale

        self.data = self.ReadHGT(path)
        self.top_left = list(start_loc)
        self.bottom_right = [start_loc[0] + (point_scale[0] * shape[0]), start_loc[1] + (point_scale[1] * shape[1])]

    # Function to read HGT data from the path, reading as small endian 4 byte floats
    def ReadHGT(self, path):

        hgt_file = open(path, "rb")
        data_arr = np.empty(shape=self.shape, dtype=np.float32)

        for i in range(self.shape[0]):

            for j in range(self.shape[1]):

                data = hgt_file.read(4)

                data_arr[i][j] = struct.unpack('<f', data)[0]

        return data_arr

# Gets minimum from a 2D array but also handles for the edge case of all the -10000 points that are given in a HGT file
def GetMin(arr):

    cur_min = 10000000000000000000
    shape = arr.shape
    for i in range(shape[0]):

        for j in range(shape[1]):

            if cur_min > arr[i][j] and arr[i][j] > -100:
                cur_min = arr[i][j]
            
    return cur_min

# Gets maxmimum from a 2D array but also handles for the edge case of all the -10000 points that are given in a HGT file (This is relevant for max function after we get the difference between points and resample the data)
def GetMax(arr):

    cur_max = -10000000000000000000
    shape = arr.shape
    for i in range(shape[0]):

        for j in range(shape[1]):

            if cur_max < arr[i][j] and arr[i][j] < 3000:
                cur_max = arr[i][j]
            
    return cur_max

# Takes a HGTData, top left corner and the bottom right corner of the lat and long rectangle, then clips the HGTData array based on how many points it has outside the rectangle
def ClipRectangle(data, abs_top_left, abs_bottom_right):

    lat_start = 0
    long_start = 0

    lat_end = data.data.shape[0]
    long_end = data.data.shape[1]

    if data.top_left[0] > abs_top_left[0]:

        clip_length = data.top_left[0] - abs_top_left[0]
        lat_start = int(round(abs(clip_length / data.point_scale[0])))

    if data.top_left[1] > abs_top_left[1]:

        clip_length = data.top_left[1] - abs_top_left[1]
        long_start = int(round(abs(clip_length / data.point_scale[1])))

    if data.bottom_right[0] < abs_bottom_right[0]:

        clip_length = data.bottom_right[0] - abs_bottom_right[0]
        lat_end -= int(round(abs(clip_length / data.point_scale[0])))

    if data.bottom_right[1] < abs_bottom_right[1]:

        clip_length = data.bottom_right[1] - abs_bottom_right[1]
        long_end -= int(round(abs(clip_length / data.point_scale[1])))

    data.data = data.data[long_start:long_end, lat_start:lat_end]

# Resamples a HGTData based on a scale factor
def ResizeData(data, scale_factor):

    data.data = cv2.resize(data.data, None, fx=scale_factor[1], fy=scale_factor[0])

# Begins reading in and handling data
# Lots of comments in this section that can be uncommented to see data, not important unless curious. Some is computationally expensive and only run once for an output
glacier_1 = HGTData("glacier_1.hgt", DATA_SHAPE_1, START_LOC_1, POINT_SCALE_1)
glacier_2 = HGTData("glacier_2.hgt", DATA_SHAPE_2, START_LOC_2, POINT_SCALE_2)

# Gets the corners of the latitude and longitude rectangle that will be covered by the data
# This is done by taking the largest possible rectangle but still allowing for each HGT to cover every single point in it's bounds
absolute_top_left = [min(glacier_1.top_left[0], glacier_2.top_left[0]), max(glacier_1.top_left[1], glacier_2.top_left[1])]
absolute_bottom_right = [max(glacier_1.bottom_right[0], glacier_2.bottom_right[0]), min(glacier_1.bottom_right[1], glacier_2.bottom_right[1])]

# print(absolute_top_left)
# print(absolute_bottom_right)

# Clips each HGTData
ClipRectangle(glacier_1, absolute_top_left, absolute_bottom_right)
ClipRectangle(glacier_2, absolute_top_left, absolute_bottom_right)

# print(glacier_1.data.shape)
# print(glacier_2.data.shape)

# print(max(GetMax(glacier_1.data), GetMax(glacier_2.data))) # 647.0
# print(min(GetMin(glacier_1.data), GetMin(glacier_2.data))) # 1770.0

# Determine amount of down-scaling needed. Only do as much as required at this point
glacier_1_scale_factor = (min(glacier_2.data.shape[0] / glacier_1.data.shape[0], 1), min(glacier_2.data.shape[1] / glacier_1.data.shape[1], 1))
glacier_2_scale_factor = (min(glacier_1.data.shape[0] / glacier_2.data.shape[0], 1), min(glacier_1.data.shape[1] / glacier_2.data.shape[1], 1))

ResizeData(glacier_1, glacier_1_scale_factor)
ResizeData(glacier_2, glacier_2_scale_factor)

# print(glacier_1.data.shape)
# print(glacier_2.data.shape)

# Determine the different between each HGTData, but has a check to prevent -10000s from causing damage
# Certain numbers, like the 647 used here, are gotten from the min and max function but are only run once then hard coded because of extensive computations those functions need
glacier_diff_shape = glacier_1.data.shape
glacier_diff = np.empty(glacier_diff_shape, dtype=np.float32)

for i in range(glacier_diff_shape[0]):
    for j in range(glacier_diff_shape[1]):

        if glacier_1.data[i][j] < 647 or glacier_2.data[i][j] < 647:
            glacier_diff[i][j] = -10000
        else:
            glacier_diff[i][j] = glacier_2.data[i][j] - glacier_1.data[i][j]

# print(GetMax(glacier_diff))
# print(GetMin(glacier_diff))

# Saves the arrays as numpy pickles to be used later
with open("glacier_1.pickle", 'wb') as file:
    pickle.dump(glacier_1.data, file)

with open("glacier_2.pickle", 'wb') as file:
    pickle.dump(glacier_2.data, file)

with open("glacier_diff.pickle", 'wb') as file:
    pickle.dump(glacier_diff, file)

# Runtime check for optimization
runtime = int(time.time() - start_time)
hours, remainder = divmod(runtime, 3600)
minutes, seconds = divmod(remainder, 60)

print(f"Runtime: {minutes} minutes, {seconds} seconds")