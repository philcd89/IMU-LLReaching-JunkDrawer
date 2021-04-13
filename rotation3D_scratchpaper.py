# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 18:07:14 2021

@author: philc
"""
#%% Setup
import scipy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math as m

from scipy.spatial.transform import Rotation as R


#%% Load data
demoData = pd.read_table("rotation_demo.txt", sep = ",")
 #Use 3d rotation matrix to negate any rotation around x(?) axis
# theta = R.from_euler('x', flat_list[21])
# r_new = theta.as_euler('zyx')

#%% Isolate arrays
# Get arrays for channels of interest (Right shank (Node03))
rx_og = np.asarray(demoData.loc[:, "Node03.rx"])
ry_og = np.asarray(demoData.loc[:, "Node03.ry"])
rz_og = np.asarray(demoData.loc[:, "Node03.rz"])

#%% Take a look at data
def plotdata(x, y, z):
    fig, ax = plt.subplots(3)

    ax[0].plot(x)
    ax[1].plot(y)
    ax[2].plot(z)

    plt.setp(ax, ylim = (-m.pi, m.pi))

plotdata(rx_og, ry_og, rz_og)

#%% Fix pi crossings.

for i in range(len(rx_og)-1):
    if rx_og[i] > 0:
        rx_og[i] -= 2*m.pi
    # if ry_og[i] > 0:
    #     ry_og[i] -= 2*m.pi
    if rz_og[i] < 0:
        rz_og[i] += 2*m.pi

plotdata(rx_og, ry_og, rz_og)

#%% Perform Rotations

#Initialize empty rotated vectors
rx_rot = np.zeros(len(rx_og))
ry_rot = np.zeros(len(ry_og))
rz_rot = np.zeros(len(rz_og))

#Perform rotation
for i in range(len(rx_og)-1):
    
    sensor_rot = np.array([rx_og[i], ry_og[i], rz_og[i]])
    rotation_axis = np.array([-1,0,0]) #reverse x-axis rotation

    rotation_vector = sensor_rot * rotation_axis
    rotation = R.from_euler("xyz", rotation_vector)
    rotated_angs = rotation.apply(sensor_rot)
    rx_rot[i] = rotated_angs[0]
    ry_rot[i] = rotated_angs[1]
    rz_rot[i] = rotated_angs[2]
    
#%% Take a look at new data

plotdata(rx_rot, ry_rot, rz_rot)
