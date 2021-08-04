#!/usr/bin/env python

"""
@Author: Antonio Andriella
This file has a class which defines the skin of the baxter's face.
Credits to Bilgehan NAL for creating the whole package for the Baxter robot
"""

from PIL import Image
import rospy

class Skin:
    
    indexOfSkin = 1 # choosen element of the array

    def __init__(self, folder_path, initSkin):

        # This array keeps the diffirent colour version of skin
        self.skins = [
            Image.open(folder_path+"skin.png")
        ]



        self.indexOfSkin = initSkin
    

    # Encapsulation 

    def setSkin(self, skinNo):
        self.indexOfSkin = skinNo

    def getSkin(self):
        return self.skins[self.indexOfSkin]