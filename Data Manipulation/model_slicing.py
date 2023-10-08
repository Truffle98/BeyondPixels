# Title: model_slicing
# Author: Daniel Álvarez Carreño
# Takes in an stl file and slices it in pins

import numpy as np
import trimesh
from itertools import product
from multiprocessing import Process, Manager

# Load model in
mesh = trimesh.load('sliced.stl')
# Is it watertight
print(mesh.is_watertight)


# Get coordinates of bounding box to find the length of the model
coordinates = trimesh.bounds.corners(mesh.bounding_box.bounds)
x = coordinates[1][0] - coordinates[0][0]

# Target dimensions for square. Units are the same as the model.
# Input model should be in mm
L = 100

A = L/x
mesh.apply_scale(A)

# Get coordinates of bounding box.
# Take only the first 4. Coordinates of the base of the box
coordinates = trimesh.bounds.corners(mesh.bounding_box.bounds)

coordinates = trimesh.bounds.corners(mesh.bounding_box.bounds)
coord_base = coordinates[:4]
print(coord_base)
x = coord_base[1][0] - coord_base[0][0]
y = coord_base[0][1] - coord_base[3][1]

# Pixels per axis
n = 10

dx = x/n
dy = y/n
ds = 0.5

# Generate a scene to visualize the model
scene = trimesh.Scene()
slices = []

def slicing(bounds, return_list):
    # print(f"j={j}, i={i}")
    box = trimesh.creation.box(bounds=bounds)
    # Split the mesh. AND boolean operation
    splitted_mesh = mesh.slice_plane(box.facets_origin, -box.facets_normal, cap=True)
    # Checker board pattern to see the pixelation
    if((i+j)%2):
        splitted_mesh.visual.face_colors = [0.5, 0.5, 0.5, 0.5]
        
    return_list.append(splitted_mesh)
    print(f"\rSlicing: {np.size(return_list)/n**2*100:.2f}%", end='')
    
    
# Box for pixelation
# i -> x
# j -> y
pixels = product(range(n), range(n))

# Use multiprocessing to speed up the process
processes = []
manager = Manager()
return_list = manager.list()
for element in list(pixels):
    i = element[0]
    j = element[1]
    # Bounds of pixelation bos
    # Negative y moves the boxes in the positive direction
    bounds = [[coordinates[0][0]+dx*i, coordinates[0][1]-dy*j, coordinates[0][2]],
            [coordinates[4][0]+dx*(i+1) - ds, coordinates[5][1]-dy*(j+1) - ds, coordinates[6][2]]]
    
    # Limit to 8 processes, one per core
    if len(processes) < 8:
        p = Process(target=slicing, args=(bounds,return_list, ))
        p.start()
        processes.append(p)
        
    else:
        for process in processes:
            process.join()
            
        processes = []
        p = Process(target=slicing, args=(bounds,return_list, ))
        p.start()
        processes.append(p)

for process in processes:
    process.join()

# Join all the slices together
final_sliced = return_list[0]
for slice in return_list[1:]:
    final_sliced += slice
    
scene.add_geometry(final_sliced)
scene.add_geometry(trimesh.creation.axis(axis_radius=2, axis_length=100))
# Export and show
trimesh.exchange.export.export_mesh(final_sliced, 'sliced_processed.stl')

scene.show()