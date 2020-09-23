#import collada
#mport pywavefront
import numpy as np
from collada import *
#from stl import mesh

#msh = collada.Collada('/home/naik/ground.dae')
#scene = pywavefront.Wavefront('/home/naik/ground.obj', create_materials=True, collect_faces=True)
#my_mesh = mesh.Mesh.from_file('/home/naik/ground.stl')

vertices = np.loadtxt('vertices.csv', delimiter=',')
normals = np.loadtxt('normals.csv', delimiter=',')
ind = np.loadtxt('indices.csv', delimiter=',')

reformed_ind = np.zeros((normals.shape[0], 3, 2))

for i in range(0, normals.shape[0]):
    reformed_ind[i][0][0] = ind[i][0]
    reformed_ind[i][1][0] = ind[i][1]
    reformed_ind[i][2][0] = ind[i][2]
    reformed_ind[i][0][1] = 4 * i
    reformed_ind[i][1][1] = (4 * i) + 1
    reformed_ind[i][2][1] = (4 * i) + 2

normals_4 = np.zeros((normals.shape[0] * 4, normals.shape[1]))
for i in range(0, normals.shape[0]):
    normals_4[4 * i] = normals[i]
    normals_4[(4*i) + 1] = normals[i]
    normals_4[(4*i) + 2] = normals[i]
    normals_4[(4*i) + 3] = normals[i]

vertices = np.ravel(vertices, order='C')
normals_4 = np.ravel(normals_4, order='C')
reformed_ind = np.ravel(reformed_ind, order='C')
reformed_ind = reformed_ind.astype(int)

mesh = Collada()
effect = material.Effect("effect0", [], "phong", diffuse=(1,1,1), specular=(0,1,0))
mat = material.Material("material0", "mymaterial", effect)
mesh.effects.append(effect)
mesh.materials.append(mat)

vert_src = source.FloatSource("verts-array", np.array(vertices), ('X', 'Y', 'Z'))
normal_src = source.FloatSource("normals-array", np.array(normals_4), ('X', 'Y', 'Z'))

geom = geometry.Geometry(mesh, "geometry0", "myground", [vert_src, normal_src])

input_list = source.InputList()
input_list.addInput(0, 'VERTEX', "#verts-array")
input_list.addInput(1, 'NORMAL', "#normals-array")

indices = np.array([3,0,1,1,0,2,2,4,3,5,0,6])

triset = geom.createTriangleSet(reformed_ind, input_list, "materialref")

geom.primitives.append(triset)
mesh.geometries.append(geom)

matnode = scene.MaterialNode("materialref", mat, inputs=[])
geomnode = scene.GeometryNode(geom, [matnode])
node = scene.Node("node0", children=[geomnode])

myscene = scene.Scene("myscene", [node])
mesh.scenes.append(myscene)
mesh.scene = myscene

mesh.write('generated_ground.dae')

print(mesh)