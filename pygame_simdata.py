# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:28:28 2021

@author: philc
"""

#%% Setup
import pandas as pd
import sys
import pygame
import time
from win32api import GetSystemMetrics as SysMet

#%% Import data
demoData = pd.read_table("r_sit_data.txt", sep = ",")

#%% Initialize game
pygame.init()

#initialize game screen
width = SysMet(0)
height = round(SysMet(1)*0.92) # 95-ish% of screen height, to allow for window bar to be seen
screen = pygame.display.set_mode((width, height))

#%% Window title
pygame.display.set_caption("Basic Reaching Task")
# icon = pygame.image.load("imagename.png")
# pygame.display.set_icon(icon)

#%% Set target parameters

# Home Position Parameters
HomeX = round(width/2)
HomeY = round(height*0.75) # 3/4 down screen from bottom
HomeRad = 20

# Target Parameters
TargX = round(width/2)
TargY = HomeY - 400
TargRad = 20

# Cursor Parameters
CursX = round(width/2)
CursY = HomeY
CursRad = 12

def HomePos():
    pygame.draw.circle(screen, (255, 0, 0), (HomeX, HomeY), HomeRad)
    
def TargPos():
    pygame.draw.circle(screen, (255, 0, 0), (TargX, TargY), TargRad)

def CursPos():
    pygame.draw.circle(screen, (255, 255, 255), (CursX, CursY), CursRad)    

#%% Main game loop
run = True
i = 0

#Initial state of rz (flexion/extension) and ry (abduction/adduction)
rz_init = demoData.loc[0, "Node03.rz"]
ry_init = demoData.loc[0, "Node03.ry"]

#Set Gain factor
yGain = 800 # y cursor movement controlled by rz 
xGain = 800 # x cursor movement controlled by ry

try:
    while run == True:
        
        # persistent parameters should stay in while loop
        
        pygame.mouse.set_visible(False)
        
        screen.fill((0,0,0)) # black
        HomePos()
        #TargPos()
        
        if(i == 0):
            CursX = HomeX
            CursY = HomeY
        else:
            CursX = HomeX - ((demoData.loc[i, "Node03.ry"] - ry_init)*xGain)
            CursY = HomeY + ((demoData.loc[i, "Node03.rz"] - rz_init)*yGain)
        CursPos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
        
        i += 1
        
        time.sleep(0.01)
        
except KeyboardInterrupt:
    sys.exit("User quit game")