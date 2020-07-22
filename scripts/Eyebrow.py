#!/usr/bin/env python

"""
@Author: Antonio Andriella
This file has a class which defines the eyebrow of the Tiago's face.
Credits to Bilgehan NAL
"""

from PIL import Image
import rospy

class Eyebrow:

    indexOfEyebrow = 0  # choosen element of the array

    def __init__(self, folder_path, initEyebrow):
        # This array keeps the diffirent shape of eyebrow
        self.eyebrows = [
            Image.open(folder_path+"eye_brow_neutral.png"),
            Image.open(folder_path+"eye_brow_happy.png"),
            Image.open(folder_path+"eye_brow_sad.png"),
            Image.open(folder_path+"eye_brow_confused.png"),
            Image.open(folder_path+"eye_brow_angry.png")
        ]

        self.indexOfEyebrow = initEyebrow
    

    # Encapsulation

    def setEyebrow(self, eyebrow):
        self.indexOfEyebrow = eyebrow

    def getEyebrow(self):
        print "index eyebrow ",self.indexOfEyebrow
        return self.eyebrows[self.indexOfEyebrow]