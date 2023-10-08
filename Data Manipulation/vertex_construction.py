import pickle
import numpy as np
import open3d as o3d
from itertools import product
from stl import mesh
import trimesh
from numpy.random import uniform

with open('test_image.pickle', 'rb') as f:
    data = pickle.load(f)
    



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
    x = element[0]
    y = element[1]
    z = np.average(data[element[0]][element[1]])
    
    
    
def surface_edge_to_faces(edge_virtex_indices, base_indices):
    """
    edge_virtex_indices: [V_i_0, ..., V_i_n] list of the indices of a given edge
    base_indices: [A, B]¡ents which are the indices of the bottom corners associated with that edge

    return a list of faces 
    """ 
    edge = len(data)
    
    # coord = 
    # for V in edge_virtex_indices:
    #     if (V < edge):
            
    



def surface_to_edges(array):
    """
    Takes array describing the surface
    returns list length 4, where each index is an array of indexes of the vertices describing the surface edge boundary

    [Edge1_listofvertices, Edge2_list_ofvertices, Edge3_list_ofvertices, Edge4_list_ofvertices]
    """
    
    
    