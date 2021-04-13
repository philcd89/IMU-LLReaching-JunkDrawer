# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 14:09:55 2021

@author: philc
"""
#%% Get relevent modules

import numpy as np
import pandas as pd
import itertools
import time
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

#%% Get demo data that was collected by me 

demoData = pd.read_table("r_sit_data.txt", sep = ",")

# def datasim(row = i, data = demoData, channel = "Node03.lax"):
#     print(data.loc[row,channel])
#     return(data.loc[row, channel])

# for i in range(1,len(demoData)):
#     datasim()


# If I want to create continuous loop...
# contData = itertools.cycle(demoData['Node03.lax'])

#%% Generate functions

def shiftnadd(list_to_shift, val_to_add):
    newlist = list_to_shift[1:] # drop first sample
    newlist = np.append(newlist, val_to_add) # append new sample to end of window  
    return(newlist)

def plotlivedata(data):
    plt.clf()
    plt.plot(range(0,300), data)
    plt.pause(0.000001)

#%% Main data loop
try:
    plotWindow = 3 #seconds: sampling rate of sensors is 100 Hz
    RShank_rx = np.zeros(plotWindow*100) # initialize empty vectors for plotting at 100 Hz
    RShank_ry = np.zeros(plotWindow*100)
    RShank_rz = np.zeros(plotWindow*100)
    
    fig = plt.figure()
    
    # ---------- MAIN CONTROL LOOP -----------
    # use rz because when IMU is placed on side of leg, rz roughly tracks flexion/extension
    for i in demoData['Node03.rz']:
        
        # -------- PRINT TO CONSOLE ---------
        print(i)
        
        # -------- UPDATE THE DATA ARRAY WITH NEW DATA --------
        RShank_rz = shiftnadd(RShank_rz, i)

        # -------- PLOT LIVE DATA ----------
        # FuncAnimation(plt.gcf(), plotlivedata, interval = 10)  
        plotlivedata(RShank_rz)
        
        
        
        
        # -------- CYCLE LOOP AT SPECIFIED SAMPLE RATE ---------
        time.sleep(0.001)

except KeyboardInterrupt:
    sys.exit("User interrupt")
    
#%% Or just plot the data....

def roll_x(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
        return roll_x

def pitch_y(x, y, z, w):
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
        return pitch_y
        
def yaw_z(x, y, z, w):
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
        return yaw_z
     
        # return roll_x, pitch_y, yaw_z # in radians



demoData = pd.read_table("demo.txt", sep = ",")

plt.plot(demoData["Node03.Lqw"])
plt.show()
plt.plot(demoData["Node03.Lqx"])
plt.show()
plt.plot(demoData["Node03.Lqy"])
plt.show()
plt.plot(demoData["Node03.Lqz"])
plt.show()

plt.plot(demoData["Node03.rx"])
plt.show()
plt.plot(demoData["Node03.ry"])
plt.show()
plt.plot(demoData["Node03.rz"])
plt.show()

roll_x_eul = np.zeros(1000)
pitch_y_eul = np.zeros(1000)
yaw_z_eul = np.zeros(1000)
for i in range(len(roll_x_eul)):
    roll_x_eul[i] = roll_x(demoData.loc[i,"Node03.Lqx"], demoData.loc[i,"Node03.Lqy"], demoData.loc[i,"Node03.Lqz"], demoData.loc[i,"Node03.Lqw"])
    pitch_y_eul[i] = pitch_y(demoData.loc[i,"Node03.Lqx"], demoData.loc[i,"Node03.Lqy"], demoData.loc[i,"Node03.Lqz"], demoData.loc[i,"Node03.Lqw"])
    yaw_z_eul[i] = yaw_z(demoData.loc[i,"Node03.Lqx"], demoData.loc[i,"Node03.Lqy"], demoData.loc[i,"Node03.Lqz"], demoData.loc[i,"Node03.Lqw"])
    
plt.plot(roll_x_eul)
plt.show()
plt.plot(pitch_y_eul)
plt.show()
plt.plot(yaw_z_eul)
plt.show()

plt.plot(demoData["Node03.Gwq"])
plt.show()
plt.plot(demoData["Node03.Gqx"])
plt.show()
plt.plot(demoData["Node03.Gqy"])
plt.show()
plt.plot(demoData["Node03.Gqz"])
plt.show()

