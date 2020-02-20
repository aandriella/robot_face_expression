#!/usr/bin/env python

"""
@Author: Bilgehan NAL
This file has a class which defines the skin of the baxter's face.
"""

from PIL import Image
import rospy

class Skin:
    
    indexOfSkin = 5 # choosen element of the array

    def __init__(self, initSkin):

        # This array keeps the diffirent colour version of skin
        self.skins = [
            Image.open("test/skin.png"),
            Image.open("test/skin.png"),
            Image.open("test/skin.png"),
            Image.open("test/skin.png"),
            Image.open("test/skin.png"),
            Image.open("test/skin.png")

        ]



        self.indexOfSkin = initSkin
    

    # Encapsulation 

    def setSkin(self, skinNo):
        self.indexOfSkin = skinNo

    def getSkin(self):
        return self.skins[self.indexOfSkin]