import numpy as np

# Class that makes colorful topology maps
class ColourConverter(object):

    # Can initialize with different colors and ranges
    def __init__(self, colours = ((153, 255, 0), (0, 240, 120), (0, 240, 240), (0, 180, 240), (0, 0, 255)), thresholds = (0, 0.25, 0.5, 0.75, 1)):
        self.colours = colours
        self.thresholds = thresholds

    # Blends a number between two colors
    def colour_blender(self, colour1, colour2, colour_percent):
        colour_percent2 = 1 - colour_percent 
        mixed_colour = (
            int((colour1[0] * colour_percent2) + (colour2[0] * colour_percent)),
            int((colour1[1] * colour_percent2) + (colour2[1] * colour_percent)),
            int((colour1[2] * colour_percent2) + (colour2[2] * colour_percent)) )
        return mixed_colour
    
    # Converts a normalized array into a colorful image based on the colors and thresholds
    def colour_function(self, numpy_array):

        colour_array = np.empty(shape = (len(numpy_array), len(numpy_array[0]), 3), dtype=np.uint8) # dtype used for an image

        for i in range(len(numpy_array)):
            for j in range(len(numpy_array[0])):
                for s in range(4):
                    if (numpy_array[i][j] <= self.thresholds[s + 1]):
                        for k in range(3):
                            var1 = (numpy_array[i][j]) - self.thresholds[s]
                            colour_percent = var1/(self.thresholds[s + 1] - self.thresholds[s])
                            mixed_colour = self.colour_blender(self.colours[s], self.colours[s + 1], colour_percent)
                            colour_array[i][j][k] = mixed_colour[k]
                        break
        
        return colour_array