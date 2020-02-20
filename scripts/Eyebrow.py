#!/usr/bin/env python

"""
@Author: Bilgehan NAL
This file has a class which defines the mouth of the baxter's face.
"""

from PIL import Image
import rospy

class Eyebrow:

    indexOfEyebrow = 0  # choosen element of the array

    def __init__(self, initEyebrow):
        # This array keeps the diffirent shape of eyebrow
        self.eyebrows = [
            Image.open("test/eye_brow_neutral.png"),
            Image.open("test/eye_brow_happy.png"),
            Image.open("test/eye_brow_sad.png"),
            Image.open("test/eye_brow_confused.png"),
            Image.open("test/eye_brow_angry.png")
            #Image.open("data/"+self.robot_gender+"/eyebrow/baxter_eyebrow_3.png"),
            #Image.open("data/"+self.robot_gender+"/eyebrow/baxter_eyebrow_4.png")
        ]

        self.indexOfEyebrow = initEyebrow
    

    # Encapsulation

    def setEyebrow(self, eyebrow):
        self.indexOfEyebrow = eyebrow

    def getEyebrow(self):
        print "index eyebrow ",self.indexOfEyebrow
        return self.eyebrows[self.indexOfEyebrow]