# -*- coding: utf-8 -*-
"""
Develop Displacement Algorithm

Created on Fri Feb  5 13:24:36 2021

@author: philc
"""
#%% Import Modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.integrate as integrate


#%% Load demo data

# Demo data was collected across 1 minute of repeatedly moving foot foward/back, left/right, up/down
demoData = pd.read_table("demo.txt", sep = ",")
RShank_demoData = demoData[["sampleNum", "Node03.lax", "Node03.lay", "Node03.laz", "Node03.rx", "Node03.ry", "Node03.rz"]]

#%% Visualize data

fig1, (ax1, ax2, ax3) = plt.subplots(nrows = 3, ncols = 1)

ax1.plot(RShank_demoData["sampleNum"], RShank_demoData["Node03.lax"], label = "Acc X")
ax1.set_title("X Acceleration")
ax1.set_ylabel("X Acc (m/s/s)")

ax2.plot(RShank_demoData["sampleNum"], RShank_demoData["Node03.lay"], label = "Acc Y")
ax2.set_title("Y Acceleration")
ax2.set_ylabel("Y Acc (m/s/s)")

ax3.plot(RShank_demoData["sampleNum"], RShank_demoData["Node03.laz"], label = "Acc Z")
ax3.set_title("Z Acceleration")
ax3.set_ylabel("Z Acc (m/s/s)")
ax3.set_xlabel("Samples")

plt.show()

fig2, (ax1, ax2, ax3) = plt.subplots(nrows = 3, ncols = 1)

ax1.plot(RShank_demoData["sampleNum"], RShank_demoData["Node03.rx"], label = "Angle X")
ax1.set_title("X Euler Angle")
ax1.set_ylabel("X Angle (deg)")

ax2.plot(RShank_demoData["sampleNum"], RShank_demoData["Node03.ry"], label = "Angle Y")
ax2.set_title("Y Euler Angle")
ax2.set_ylabel("Y Angle (deg)")

ax3.plot(RShank_demoData["sampleNum"], RShank_demoData["Node03.rz"], label = "Angle Z")
ax3.set_title("Z Euler Angle")
ax3.set_ylabel("Z Angle (deg)")
ax3.set_xlabel("Samples")

plt.show()

#%% raw double integration, just for shits and giggles

srate = 0.01

RShank_demoData["Node03.lvx"] = integrate.cumtrapz(RShank_demoData["Node03.lax"], initial = 0)  # First integration
RShank_demoData["Node03.lvy"] = integrate.cumtrapz(RShank_demoData["Node03.lay"], initial = 0)  
RShank_demoData["Node03.lvz"] = integrate.cumtrapz(RShank_demoData["Node03.laz"], initial = 0)
RShank_demoData["Node03.lsx"] = integrate.cumtrapz(RShank_demoData["Node03.lvx"], initial = 0)  # Second integration
RShank_demoData["Node03.lsy"] = integrate.cumtrapz(RShank_demoData["Node03.lvy"], initial = 0)
RShank_demoData["Node03.lsz"] = integrate.cumtrapz(RShank_demoData["Node03.lvz"], initial = 0)

fig3, (ax1, ax2, ax3) = plt.subplots(nrows = 3, ncols = 1)

ax1.plot(RShank_demoData["sampleNum"], RShank_demoData["Node03.lvx"], label = "Vel X")
ax1.set_title("X Velocity")
ax1.set_ylabel("X Vel (m/s)")

ax2.plot(RShank_demoData["sampleNum"], RShank_demoData["Node03.lvy"], label = "Vel Y")
ax2.set_title("Y Velocity")
ax2.set_ylabel("Y Vel (m/s)")

ax3.plot(RShank_demoData["sampleNum"], RShank_demoData["Node03.lvz"], label = "Vel Z")
ax3.set_title("Z Velocity")
ax3.set_ylabel("Z Vel (m/s)")
ax3.set_xlabel("Samples")

plt.show()

fig4, (ax1, ax2, ax3) = plt.subplots(nrows = 3, ncols = 1)

ax1.plot(RShank_demoData["sampleNum"], RShank_demoData["Node03.lsx"], label = "Disp X")
ax1.set_title("X Displacement")
ax1.set_ylabel("X Disp (m)")

ax2.plot(RShank_demoData["sampleNum"], RShank_demoData["Node03.lsy"], label = "Disp Y")
ax2.set_title("Y Displacement")
ax2.set_ylabel("Y Disp (m)")

ax3.plot(RShank_demoData["sampleNum"], RShank_demoData["Node03.lvz"], label = "Vel Z")
ax3.set_title("Z Displacement")
ax3.set_ylabel("Z Disp (m)")
ax3.set_xlabel("Samples")

plt.show()

# Conclusion - sensors are all badly drifting.  Need to figure out how to correct this.




