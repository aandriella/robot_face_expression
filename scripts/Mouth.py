#!/usr/bin/env python

"""
@Author: Bilgehan NAL
This file has a class which defines the mouth of the baxter's face.
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