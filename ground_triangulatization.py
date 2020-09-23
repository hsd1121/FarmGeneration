from scipy.spatial import Delaunay
import numpy as np
import matplotlib.pyplot as plt
from sympy import Plane, Point3D
import math

height_variation = 0
grid_size = 0
num_of_vertices = 0

param_file = open('ground_params.txt', 'r')
lines = param_file.readlines()

count = 0
for line in lines:
    if count == 0:
        grid_size = int(line)
    elif count == 1:
        num_of_vertices = int(line)
    elif count == 2:
        height_variation = float(line)
    count = count + 1

points = np.random.random([num_of_vertices, 2])
end_vertices = np.array([[-0.5 * grid_size, -0.5 * grid_size], [-0.5 * grid_size, 0.5 * grid_size], [0.5 * grid_size, -0.5 * grid_size], [0.5 * grid_size, 0.5 * grid_size]])
points = points * grid_size
points = points - (grid_size / 2)
points = np.append(points, end_vertices, axis=0)
tri = Delaunay(points)

indices = np.asarray(tri.simplices)
plt.triplot(points[:,0], points[:,1], tri.simplices)
plt.plot(points[:,0], points[:,1], 'o')
plt.show()

points_3d = np.random.random((points.shape[0], 3))
points_3d = (-1 * height_variation / 2) + (points_3d * height_variation)

points_3d[:,0] = points[:,0]
points_3d[:,1] = points[:,1]

all_normals = np.zeros((1,3))

count = 0

for item in tri.simplices:
    point1 = points_3d[item[0]]
    point2 = points_3d[item[1]]
    point3 = points_3d[item[2]]
    triangle = Plane(Point3D(point1[0], point1[1], point1[2]), Point3D(point2[0], point2[1], point2[2]), Point3D(point3[0], point3[1], point3[2]))
    normal = np.zeros((1,3))
    normal[0][0] = float(triangle.normal_vector[0])
    normal[0][1] = float(triangle.normal_vector[1])
    normal[0][2] = float(triangle.normal_vector[2])

    mag = (normal[0][0] * normal[0][0]) + (normal[0][1] * normal[0][1]) + (normal[0][2] * normal[0][2])
    mag = math.sqrt(mag)
    normal[0][0] = normal[0][0] / mag
    normal[0][1] = normal[0][1] / mag
    normal[0][2] = normal[0][2] / mag

    if count == 0:
        count = count + 1
        all_normals[0,:] = normal
    else:
        all_normals = np.append(all_normals, normal, axis=0)

np.savetxt('vertices.csv', points_3d, delimiter=',')
np.savetxt('normals.csv', all_normals, delimiter=',')
np.savetxt('indices.csv', indices, delimiter=',')