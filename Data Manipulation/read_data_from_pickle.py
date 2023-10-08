import pickle
import numpy as np
import open3d as o3d
from itertools import product
from stl import mesh
import trimesh
from numpy.random import uniform
import cv2


# data = cv2.imread("glacier/Glacier_1.png")

with open('test_image.pickle', 'rb') as f:
    data = pickle.load(f)
    
print(np.min(data), np.max(data))


i = product(range(len(data)), range(len(data)))
# # print(list(i))

X = []
Y = []
Z = []
# data_in_coord = "<X> <Y> <Z>\n"
points = []
for element in list(i):
    x = element[0]
    y = element[1]
    z = np.average(data[element[0]][element[1]])
    X.append(x)
    Y.append(y)
    Z.append(z)
    points.append([x, y, z])
    
low_z = np.min(Z)
print(np.min(data), np.max(data))

print(data.shape)
# y = np.linspace()
n_points = int(len(data)/2)
i = product(range(n_points), range(n_points))
sampling_points = np.linspace(0, len(data), n_points)

for j in list(i):
    y = sampling_points[j[0]]
    x = sampling_points[j[1]]
    points.append([x, y, low_z])


# i = product(range(n_points), range(n_points))
sampling_points_y = np.linspace(0, len(data), n_points)
sampling_points_x = np.linspace(0, len(data), n_points)

# Right side
for j, point_y in enumerate(sampling_points_y):
    z = Z[int(j/n_points*len(data))]
    
    sampling_points_z = np.linspace(low_z, z, n_points)
    for point_z in sampling_points_z:
        points.append([0, point_y, point_z])
        
        
        
for j, point_x in enumerate(sampling_points_x):
    z = Z[int(len(data)*j/n_points)*len(data)]
    sampling_points_z = np.linspace(low_z, z, n_points)
    for point_z in sampling_points_z:
        points.append([point_x, 0, point_z])
        
    # x = uniform(0,len(data))
    # z = uniform(low_z, Z[int(x)*len(data)])
    # points.append([x, 0, z])


# for j in range(5000):
#     x = uniform(0,len(data))
#     z = uniform(low_z, Z[int(x)*len(data)])
#     points.append([x, 0, z])

# Back side
for j, point_x in enumerate(sampling_points_x):
    z = Z[int(j/n_points*len(data))*len(data)-1]
    sampling_points_z = np.linspace(low_z, z, n_points)
    for point_z in sampling_points_z:
        points.append([point_x, len(data), point_z])

for j, point_y in enumerate(sampling_points_y[::-1]):
    z = Z[-int(j/n_points*len(data))]
    sampling_points_z = np.linspace(low_z, z, n_points)
    for point_z in sampling_points_z:
        points.append([len(data), point_y, point_z])
        
    # Back side
    # x = uniform(0,len(data))
    # z = uniform(low_z, data[int(x)][len(data)-1][0])
    # points.append([x, len(data), z])
    
    # y = uniform(0,len(data))
    # z = uniform(low_z, Z[len(Z) - len(data) + int(y)])
    # points.append([len(data), y, z])
#     data_in_coord += f"{x} {y} {z}\n"
    
# # # with open("data.xyz", "w") as f:
# # #     f.write(data_in_coord)

import pyvista as pv

# # # points is a 3D numpy array (n_points, 3) coordinates of a sphere
cloud = pv.PolyData(points)
cloud.plot()

# surf = cloud.delaunay_3d(alpha=2.5, progress_bar=True, offset=5, tol=0.01)
surf = cloud.reconstruct_surface(nbr_sz=35, progress_bar=True)

surf.plot(show_edges=True)

# # volume = cloud.delaunay_3d(alpha=2.)
# # shell = surf.extract_geometry()
# # shell.plot()


# pl = pv.Plotter()
# _ = pl.add_mesh(surf)
# pl.export_obj('surf.obj')
    
mesh = trimesh.load("surf.obj")
# verts = mesh.faces.view(np.ndarray)
# print(verts)
# # verts[verts[:,2] == 0, 2] = z.reshape(-1)

# # # box = trimesh.creation.box(bounds=mesh.bounding_box.bounds)
# # # box.visual.face_colors = [0.5, 0.5, 0.5, 0.5]

# # # diff = trimesh.boolean.difference([box, mesh])
trimesh.repair.broken_faces(mesh)
trimesh.repair.fill_holes(mesh)
trimesh.repair.fix_inversion(mesh)

trimesh.exchange.export.export_mesh(mesh, 'sliced.stl')

(mesh).show()