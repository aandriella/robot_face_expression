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
        self.robot_gender = rospy.get_param("/robot_gender")
        # This array keeps the diffirent shape of eyebrow
        self.eyebrows = [
            Image.open("data/"+self.robot_gender+"/eyebrow/baxter_eyebrow_0.png"),
            Image.open("data/"+self.robot_gender+"/eyebrow/baxter_eyebrow_1.png"),
            Image.open("data/"+self.robot_gender+"/eyebrow/baxter_eyebrow_2.png"),
            Image.open("data/"+self.robot_gender+"/eyebrow/baxter_eyebrow_3.png"),
            Image.open("data/"+self.robot_gender+"/eyebrow/baxter_eyebrow_4.png")
        ]

        self.indexOfEyebrow = initEyebrow
    

    # Encapsulation

    def setEyebrow(self, eyebrow):
        self.indexOfEyebrow = eyebrow

    def getEyebrow(self):
        return self.eyebrows[self.indexOfEyebrow]