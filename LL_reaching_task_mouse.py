# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:28:28 2021

@author: philc
"""

#%% Setup
import sys
import pygame
import math
import numpy as np
from win32api import GetSystemMetrics as SysMet
#import win32api

#%% Get trial Conditions

# Get trial conditions
condfile = open("trial_conditions.txt", "r")
trial_conditions = np.asarray(list(map(int, condfile.readlines())))

#%% Initialize Screen and Set target parameters

#initialize colors
black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 255)

#initialize game screen
width = SysMet(0)
height = round(SysMet(1)*0.92) # 95-ish% of screen height, to allow for window bar to be seen
screen = pygame.display.set_mode((width, height))

# Set constants
centerX = round(width/2)
centerY = round(height/2)
HomeX = round(width/2)
HomeY = round(height*0.75) # 3/4 down screen from bottom
HomeRad = 20
TargX = round(width/2)
TargY = round(height*0.75) - 400
TargRad = 20
CursRad = 12
ObstY = round(height*0.75) - 300
ObstLength = 10
ObstWidth = 150

pygame.init()
pygame.display.set_caption("Basic Reaching Task")
# icon = pygame.image.load("imagename.png")
# pygame.display.set_icon(icon)

          
def Blank_Screen(color):
    screen.fill(color)
    
def Instructions(x = centerX, y = centerY):
    
    font = pygame.font.SysFont("Arial", 28)
    
    text = font.render("Instructions", True, white)
    screen.blit(text, (x - text.get_rect().width/2, y-50))
 
    text = font.render("...some instructions could go here....", True, white)
    screen.blit(text, (x - text.get_rect().width/2, y+50))
    
    text = font.render("press space to continue", True, white)
    screen.blit(text, (x - text.get_rect().width/2, y+100))
    
    pygame.display.update()

def HomePos(HomeX, HomeY, HomeRad, color):
    # Home Position Parameters
    pygame.draw.circle(screen, color, (HomeX, HomeY), HomeRad)
    
def TargPos(TargX, TargY, TargRad, color):
    # Target Parameters
    pygame.draw.circle(screen, color, (TargX, TargY), TargRad)

def CursPos(x, y, CursRad, color):
    # Cursor Parameters
    pygame.draw.circle(screen, color, (x, y), CursRad)    
    
def Obstacle(color = red, Length = ObstLength, Width = ObstWidth, x = centerX, y = ObstY):
    # Obstacle Parameters
    rect_left = x - (Width/2)
    rect_top = y
    rect_width = Width
    rect_length = Length
    RectParams = (rect_left, rect_top, rect_width, rect_length)
    pygame.draw.rect(screen, color, rect = RectParams)   
    
    
#%% INSTRUCTIONS
run = True
finished_Instructions = False

#Instructions
while run:
    
    # persistent parameters should stay in while loop
        
    # --------- GET EVENTS ---------- 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit("User quit game")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                finished_Instructions = True
    
    
    # --------- INSTRUCTIONS -----------
    
    # first, show some instructions
    Instructions()
        
    if finished_Instructions:
        Blank_Screen(black)
        pygame.display.update() 
        pygame.time.wait(2000)
        run = False
    
#%% MAIN TASK LOOP

# Define initial states
run = True    
#clock = pygame.time.Clock()
main_loop_start_time = pygame.time.get_ticks()
homeColor = red
targColor = red
sample = 1
trial = 0
curs_in_home = False
curs_in_home_time = 0
curs_in_targ = False
curs_in_targ_time = 0
move_start_time = 0
wait_in_home = 3000
hold_in_targ = 300
wait_in_targ = 2000
show_obst_pre_move = 1000
targ_hit = False

curs_in_home_prev = False
curs_in_targ_prev = False
targ_hit_prev = False
move_back_prev = False

move_back = True
move_out = False

show_obstacle = False  
trial_cond = 0

while run:
    
    # Get some constants for this loop
    pygame.mouse.set_visible(False)
    screen.fill(black)
    current_time = pygame.time.get_ticks()
    
    # Identify cursor location
    CursX = pygame.mouse.get_pos()[0]
    CursY = pygame.mouse.get_pos()[1]
    
    # Determine distances
    dist_to_home = math.sqrt((abs(CursX-HomeX)**2) + (abs(CursY-HomeY)**2))
    dist_to_targ = math.sqrt((abs(CursX-TargX)**2) + (abs(CursY-TargY)**2))
    
    # --------- IS THE CURSOR IN THE TARGET(S)? ---------
    if dist_to_home < (CursRad + HomeRad):
        curs_in_home = True
    else:
        curs_in_home = False
        
    if dist_to_targ < (CursRad + TargRad):
        curs_in_targ = True
    else:
        curs_in_targ = False
        
    # --------- LOOK FOR STATE CHANGES, GET TIME, AND CREATE EVENT ---------
    if curs_in_home and not curs_in_home_prev:
        curs_in_home_time = pygame.time.get_ticks()
        
    if not curs_in_home and curs_in_home_prev:
        move_start_time = pygame.time.get_ticks()
        
    if curs_in_targ and not curs_in_targ_prev:
        curs_in_targ_time = pygame.time.get_ticks()
        
        
    
    # ----------- MANAGE EVENTS -------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit("User quit game")
    
    
    
    
    # ----------- MAIN TRIAL LOOP ------------
    
    # Participant waits in home position, after period of time, target turns green to cue movement
    if curs_in_home and (current_time - curs_in_home_time > wait_in_home):
        cue_on = True
        targColor = green
        
    
    # Determine if the participant has begun to reach
    if not move_back and not curs_in_home and not curs_in_targ and cue_on:
        move_out = True
        
    # Participant must briefly hold in target, and signal move_out is over
    if curs_in_targ and (current_time - curs_in_targ_time > hold_in_targ):
        #play a sound?
        targ_hit = True
        move_out = False
        move_back = True
        
    # After target is hit, wait a period of time before turning target back to red
    if targ_hit and (current_time - curs_in_targ_time > wait_in_targ):
        targColor = red
        cue_on = False
                
    # Once participant leaves target, turn targ_hit to False
    if not move_out and move_back and not curs_in_home and not curs_in_targ:
        targ_hit = False
        
    # If participant is once again in home position, change move_back to False
    if curs_in_home and move_back:
        move_back = False
    
    if not move_back and move_back_prev: #if move_back switches from true to false, signalling the end of the trial, advance the trial number
        trial += 1
        
    # ---------- SET TRIAL CONDITION -----------
    
    trial_cond = trial_conditions[trial-1]
    
    # ---------- SET PRIORS ----------
    
    # Set prior states
    curs_in_home_prev = curs_in_home
    curs_in_targ_prev = curs_in_targ
    targ_hit_prev = targ_hit
    move_back_prev = move_back    
    
     # ---------- MANAGE OBSTACLE PRESENTATION ----------
    
    # No obstacle
    if trial_cond == 0:
        show_obstacle = False
    
    # Present obstacle prior to movement cue
    elif trial_cond == 1:
        if curs_in_home and (current_time - curs_in_home_time > show_obst_pre_move):
            show_obstacle = True
        elif targ_hit and (current_time - curs_in_targ_time > wait_in_targ):
            show_obstacle = False
   
    # Present obstacle with movement cue
    elif trial_cond == 2:
        if curs_in_home and (current_time - curs_in_home_time > wait_in_home):
            show_obstacle = True
        elif targ_hit and (current_time - curs_in_targ_time > wait_in_targ):
            show_obstacle = False
    
    # Present obstacle with movement onset
    elif trial_cond == 3:
        if move_out and not move_back and (current_time - curs_in_home_time > wait_in_home):
            show_obstacle = True
        elif targ_hit and (current_time - curs_in_targ_time > wait_in_targ):
            show_obstacle = False
            
    # Present obstacle when cursor is 1/3 of the way through the movement
    elif trial_cond == 4:
        if move_out and not move_back and CursY < (HomeY - (round((HomeY - TargY)/3))):
            show_obstacle = True
        elif targ_hit and (current_time - curs_in_targ_time > wait_in_targ):
            show_obstacle = False    
        
    # --------- UPDATE DISPLAY ----------    
    
    HomePos(HomeX, HomeY, HomeRad, homeColor)
    TargPos(TargX, TargY, TargRad, targColor)
    if show_obstacle:
        Obstacle()
    CursPos(CursX, CursY, CursRad, white)
    
    pygame.display.update()
    
    # ------------ SCOPE ------------
    print("targ_hit: " + str(targ_hit) + ", "  + "move_out: " + str(move_out) + ", " + "move_back: " + str(move_back) + ", " + "trial:" + str(trial))
    
pygame.quit()
    

    
