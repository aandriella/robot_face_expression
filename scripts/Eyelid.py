#!/usr/bin/env python

'''
@Author: Bilgehan NAL
This file has class which defines the eyelid of the baxter
'''

from PIL import Image
import rospy

class Eyelid:

    def __init__(self):
        self.robot_gender = rospy.get_param("/robot_gender")
        self.eyelid = Image.open("data/"+self.robot_gender+"/baxter_eyelid.png") # eyelid image
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