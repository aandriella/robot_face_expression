#!/usr/bin/env python

"""
@Author: Antonio Andriella
This file has a class which defines the mouth of the Tiago's face.
In the current version we decided to not use it
Credits to Bilgehan NAL
"""

from PIL import Image
import rospy

class Mouth:

    indexOfMouth = 0    # choosen element of the array

    def __init__(self, initMouth):

        # This array keeps the diffirent shape of mouth
        self.mouths = [

            #Image.open("data/mouth/baxter_mouth_smile_open.png")
        ]

        self.indexOfMouth = initMouth


    # Encapsulation

    def setMouth(self, mouth):
        self.indexOfMouth = mouth

    def getMouth(self):
        print(self.indexOfMouth)
        return self.mouths[self.indexOfMouth]