#!/usr/bin/env python

'''
@Author: Antonio Andriella
This file has class which defines the eyelid of the Tiago robot
Credits to Bilgehan NAL for creating the whole package for the Baxter robot
'''

from PIL import Image
import rospy

class Eyelid:

    def __init__(self, folder_path):
        self.eyelid = Image.open(folder_path+"eyelid.png") # eyelid image
        self.position = 0 # y position, we don't need x position because of vertical movment.

    def moveCalculation(self, position, destinationPosition, totalTime, instantTime):
    
        if totalTime > instantTime:
            diffirenceOfPosition = destinationPosition - position
            newPositionDiffirencePosition = float(diffirenceOfPosition)/totalTime * instantTime
            newPositionPosition = int(position + newPositionDiffirencePosition)
            self.setPosition(newPositionPosition)
            return True
        else: 
            self.setPosition(destinationPosition)
            return False

    # Encapsulation
    
    def setPosition(self, position):
        self.position = position

    def getPosition(self):
        return self.position

    def getEyelid(self):
        return self.eyelid