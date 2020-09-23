from random import seed
from random import random
from random import randint
from math import pi
import xml.etree.ElementTree as ET
import numpy as np

seed(1)


def sign(x1, y1, x2, y2, x3, y3):
    return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)


def isInside(x1, y1, x2, y2, x3, y3, x, y):

    d1 = sign(x, y, x1, y1, x2, y2)
    d2 = sign(x, y, x2, y2, x3, y3)
    d3 = sign(x, y, x3, y3, x1, y1)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not(has_neg and has_pos)


vertices = np.loadtxt('vertices.csv', delimiter=',')
normals = np.loadtxt('normals.csv', delimiter=',')
simplices = np.loadtxt('indices.csv', delimiter=',')

simplices = simplices.astype(int)
plot_width = 0
plot_length = 0
row_width = 0
row_length = 0
plants_per_plot = 0
low_scale = 0
high_scale = 0
row_params = []
model_locations = []
model_heights = []

param_file = open('params.txt', 'r')
lines = param_file.readlines()

count = 0
for line in lines:
    if count == 0:
        items = line.split()
        count2 = 0
        for item in items:
            if count2 == 0:
                plot_width = float(item)
            elif count2 == 1:
                plot_length = float(item)
            count2 = count2 + 1
    elif count == 1:
        items = line.split()
        count2 = 0
        for item in items:
            if count2 == 0:
                row_width = float(item)
            elif count2 == 1:
                row_length = float(item)
            count2 = count2 + 1
    elif count == 2:
        plants_per_plot = int(line)
    elif count == 3:
        items = line.split()
        count2 = 0
        for item in items:
            if count2 == 0:
                low_scale = float(item)
            elif count2 == 1:
                high_scale = float(item)
            count2 = count2 + 1
    else:
        row_params.append(line)
    count = count + 1

model_location_file = open('models.txt', 'r')
lines = model_location_file.readlines()
for line in lines:
    model_locations.append(line.rstrip('\n'))

model_heights_file = open("3D_Models/height.txt", "r")
lines = model_heights_file.readlines()
for line in lines:
    model_heights.append(float(line))

tree = ET.parse('empty.world')
root = tree.getroot()
model = ET.parse('soy.model')
model_root = model.getroot()

x_origin = 0
y_origin = 0

sim_heights_file = open("simulated_heights.csv", "w")
count = 1
y_count = 1
for item in row_params:
    params = item.split()

    num_of_plots = int(params[0])
    row_offset = float(params[1])
    x_origin = row_offset
    for i in range(0, num_of_plots):
        heights = ""
        for j in range(0, plants_per_plot):
            x_val = (random() * plot_width) + x_origin
            y_val = (random() * plot_length) + y_origin
            z_val = 0.0
            for k in range(0, simplices.shape[0]):
                x1 = vertices[simplices[k][0]][0]
                y1 = vertices[simplices[k][0]][1]
                x2 = vertices[simplices[k][1]][0]
                y2 = vertices[simplices[k][1]][1]
                x3 = vertices[simplices[k][2]][0]
                y3 = vertices[simplices[k][2]][1]
                z1 = vertices[simplices[k][0]][2]
                z2 = vertices[simplices[k][1]][2]
                z3 = vertices[simplices[k][2]][2]

                if isInside(x1, y1, x2, y2, x3, y3, x_val, y_val):
                    normal = normals[k]
                    d = (normal[0] * x1) + (normal[1] * y1) + (normal[2] * z1)
                    z_val = (d - (normal[0] * x_val) - (normal[1] * y_val)) / normal[2]
                    #print(z_val > 0.0)
                    #print(str(z1) + " " + str(z2) + " " + str(z3) + " " + str(z_val))
                    break

            x_scale = low_scale + (random() * (high_scale - low_scale))
            y_scale = low_scale + (random() * (high_scale - low_scale))
            z_scale = low_scale + (random() * (high_scale - low_scale))
            yaw = random() * (2 * pi)
            model_num = randint(0, 4)
            model_file = model_locations[model_num]
            pose_val = str(x_val) + " " + str(y_val) + " " + str(z_val) + " 0 0 " + str(yaw)
            scale_val = str(x_scale) + " " + str(y_scale) + " " + str(z_scale)
            soy_name = "soybean_" + str(count)
            link_name = "soybean_" + str(count) + "_link"
            col_name = "soybean_" + str(count) + "_collision"
            heights = heights + str(model_heights[model_num] * z_scale) + ","
            for model_name in model_root.iter('model'):
                model_name.set('name', soy_name)
            for model_name in model_root.iter('link'):
                model_name.set('name', link_name)
            for pose in model_root.iter('pose'):
                pose.text = pose_val
            for model_name in model_root.iter('collision'):
                model_name.set('name', col_name)
            for model_name in model_root.iter('visual'):
                model_name.set('name', soy_name)
            for scale_name in model_root.iter('scale'):
                scale_name.text = scale_val
            for model_location in model_root.iter('uri'):
                model_location.text = model_file
            for world in root.findall('world'):
                world.append(model_root)
            #print(str(x_val) + " " + str(y_val))
            count = count + 1
            tree.write('soy_plots.world')
            tree = ET.parse('soy_plots.world')
            root = tree.getroot()
        x_origin = x_origin + plot_width + row_width
        heights = heights[:-1] + "\n"
        sim_heights_file.write(heights)
    x_origin = 0
    y_origin = y_origin - plot_length - row_length
    y_count = y_count + 1

param_file.close()
model_location_file.close()