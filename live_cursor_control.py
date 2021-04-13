# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 14:01:07 2021

@author: philc

This code is a first attempt at piping MotionNode data from the path into a txt file, while also graphically representing data.
"""

#%% Setup

import argparse
import sys
import pygame
from win32api import GetSystemMetrics as SysMet

from xml.etree.ElementTree import XML

from scipy.spatial.transform import Rotation as R

import numpy as np

# import numpy as np
# import matplotlib.pyplot as plt

import MotionSDK

#%% Initialize task

pygame.init()

#initialize game screen
width = SysMet(0)
height = round(SysMet(1)*0.92) # 95-ish% of screen height, to allow for window bar to be seen
screen = pygame.display.set_mode((width, height))

#%% Window title
pygame.display.set_caption("Basic Reaching Task")
# icon = pygame.image.load("imagename.png")
# pygame.display.set_icon(icon)

#%% Set constants and target parameters

xGain = 800
yGain = 800

# Home Position Parameters
HomeX = round(width/2)
HomeY = round(height*0.75) # 3/4 down screen from bottom
HomeRad = 20

# Target Parameters
TargX = round(width/2)
TargY = HomeY - 400
TargRad = 20

# Cursor Parameters
# CursX = round(width/2)
# CursY = HomeY
# CursRad = 12

def HomePos():
    pygame.draw.circle(screen, (255, 0, 0), (HomeX, HomeY), HomeRad)
    
def TargPos():
    pygame.draw.circle(screen, (255, 0, 0), (TargX, TargY), TargRad)

# def CursPos(CursX, CursY):
#     pygame.draw.circle(screen, (255, 255, 255), (CursX, CursY), CursRad) 
    
#%%

def parse_name_map(xml_node_list):
    name_map = {}

    tree = XML(xml_node_list)

    # <node key="N" id="Name"> ... </node>
    list = tree.findall(".//node")
    for itr in list:
        name_map[int(itr.get("key"))] = itr.get("id")

    return name_map

def stream_data_to_csv(args, out):
    client = MotionSDK.Client(args.host, args.port)

    #
    # Request the channels that we want from every connected device. The full
    # list is available here:
    #
    #   https://www.motionshadow.com/download/media/configurable.xml
    #
    # Select the local quaternion (Lq) and positional constraint (c)
    # channels here. 8 numbers per device per frame. Ask for inactive nodes
    # which are not necessarily attached to a sensor but are animated as part
    # of the Shadow skeleton.
    #
    
    # ADDING linear acceleration (la) and euler angle (r) set!!!!  This should add 6 more numbers per device per frame.
    xml_string = \
        "<?xml version=\"1.0\"?>" \
        "<configurable inactive=\"1\">" \
        "<la/>" \
        "<r/>" \
        "</configurable>"

    if not client.writeData(xml_string):
        raise RuntimeError(
            "failed to send channel list request to Configurable service")

    num_frames = 0
    sample = 1
    xml_node_list = None   
    
    while True:
        
        # Block, waiting for the next sample.
        data = client.readData()
        if data is None:
            raise RuntimeError("data stream interrupted or timed out")
            break

        if data.startswith(b"<?xml"):
            xml_node_list = data
            continue

        container = MotionSDK.Format.Configurable(data)

        #
        # Consume the XML node name list. If the print header option is active
        # add that now.
        #
        if xml_node_list:
            if args.header:
                ChannelName = [
                    "lax", "lay", "laz",
                    "rx", "ry", "rz"
                ]

                name_map = parse_name_map(xml_node_list)

                flat_list = []
                for key in container:
                    if key not in name_map:
                        raise RuntimeError(
                            "device missing from name map, unable to print "
                            "header")

                    item = container[key]
                    if len(ChannelName) != item.size():
                        raise RuntimeError(
                            "expected {} channels but found {}, unable to "
                            "print header".format(
                                len(ChannelName), item.size()))

                    name = name_map[key]
                    for channel in ChannelName:
                        flat_list.append("{}.{}".format(name, channel))

                if not len(flat_list):
                    raise RuntimeError(
                        "unknown data format, unabled to print header")

                headerOut = ",".join(["{}".format(v) for v in flat_list])
                headerOut = "sampleNum," + headerOut + "," + "CursorX," + "CursorY" + "\n"
                out.write(headerOut)
                
                # out.write(
                #     ",".join(["{}".format(v) for v in flat_list]))

            xml_node_list = None

        #
        # Make an array of all of the values, in order, that are part of one
        # sample. This is a single row in the output.
        #
        flat_list = []
        for key in container:
            item = container[key]
            for i in range(item.size()):
                flat_list.append(item.value(i))

        if not len(flat_list):
            raise RuntimeError("unknown data format in stream")

        # ------------------- PYGAME CODE -----------------------
        
        pygame.mouse.set_visible(False)
        
        screen.fill((0,0,0)) # black
        HomePos()
        TargPos()
        
        if(sample == 1):
            CursX = HomeX
            CursY = HomeY
            ry_init = flat_list[22]
            rz_init = flat_list[23]
        else:
            CursX = HomeX - ((flat_list[22] - ry_init)*xGain)
            CursY = HomeY + ((flat_list[23] - rz_init)*yGain)
        #CursPos()
        pygame.draw.circle(screen, (255, 255, 255), (CursX, CursY), 12)
        
        #HomeY += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                    
        pygame.display.update()
        print(CursY)
        
        # -------------------------------------------------------
        
        dataOut = ",".join(["{}".format(round(v, 8)) for v in flat_list])
        dataOut = str(sample) + "," + dataOut + "," + str(CursX) + "," + str(CursY) + "\n"
        
        out.write(dataOut)

        sample += 1

        if args.frames > 0:
            num_frames += 1
            if num_frames >= args.frames:
                break

#%% Define input args
            
def main(argv):
    parser = argparse.ArgumentParser(
        description="")

    parser.add_argument(
        "--file",
        help="output file",
        default="")
    parser.add_argument(
        "--frames",
        help="read N frames",
        type=int, default=0)
    parser.add_argument(
        "--header",
        help="show channel names in the first row",
        action="store_true")
    parser.add_argument(
        "--host",
        help="IP address of the Motion Service",
        default="127.0.0.1")
    parser.add_argument(
        "--port",
        help="port number address of the Motion Service",
        type=int, default=32076)

    args = parser.parse_args()

    if args.file:
        with open(args.file, 'w') as f:
            stream_data_to_csv(args, f)
    else:
        stream_data_to_csv(args, sys.stdout)

#%% RUN THIS THANNGGGG
if __name__ == "__main__":
    sys.exit(main(sys.argv))