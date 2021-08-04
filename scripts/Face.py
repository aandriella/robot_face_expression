#!/usr/bin/env python

'''
@Author: Antonio Andriella
This file has a class which defines the face of Tiago
Face class has other part of the face objects.
Credits to Bilgehan NAL for creating the whole package for the Baxter robot
'''

'''
Tiago Face Descriptions:

Skin, Mouth and Eyebrow has multiple shapes.
Skin has 1a -> [0] (So far we are not interested to change the skin color of the robot)
Mouth has 7 -> [0, 6] (Not used it in the current version)
Eyebrow has 5 -> [0, 4] (neutral, happy, sad, confused, angry)

Mouth ::
    0 -> neutral mouth
    1a -> happy mouth
    2 -> sad mouth
    3 -> confused mouth
    4 -> angry mouth
Eyebrow ::
    0 -> neutral mouth
    1a -> happy mouth
    2 -> sad mouth
    3 -> confused mouth
    4 -> angry mouth
    
Coordinate range for x: [-80, 80]
Coordinate range for y: [-120, 120]

'''

from PIL import Image
import Eyebrow
import Eye
import Eyelid
import Skin
from numpy import array
import timeit
import cv2
import os
import random
import getpass
import time
import rospy

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
parent_dir_of_file = os.path.dirname(dir_path)
print(parent_dir_of_file)
class Face:

    def __init__(self):

        ''' Parts of the face of Tiago are defined.'''
        self.face_builder_path = parent_dir_of_file+"/face_builder/"
        self.backgroundImage = Image.open(self.face_builder_path+"background.png") # Background behind the eyes
        # Face partions objects
        self.skin = Skin.Skin(self.face_builder_path, 0)
        self.eye = Eye.Eye(self.face_builder_path)
        self.eyebrow = Eyebrow.Eyebrow(self.face_builder_path, 4)
        self.eyelid = Eyelid.Eyelid(self.face_builder_path)
        self.eyelid.setPosition(-330)
        self.eyesCoordinateX = self.eye.getPositionX()
        self.angleOfView = 0.25
    # buildFace function is combining the all face parts together.

    def buildFace(self):
        #self.eye = Eye.Eye("test/pupil.png")
        # Merging the layers
        faceImage = self.backgroundImage.copy()
        faceImage.paste(self.eye.getEyes(), (int(self.eye.getPositionX()), int(self.eye.getPositionY())), self.eye.getEyes())
        faceImage.paste(self.eyelid.getEyelid(), (0, self.eyelid.getPosition()), self.eyelid.getEyelid())
        faceImage.paste(self.skin.getSkin(), (0, 0), self.skin.getSkin())
        #faceImage.paste(self.mouth.getMouth(), (0, 0), self.mouth.getMouth())
        faceImage.paste(self.eyebrow.getEyebrow(), (0, 0), self.eyebrow.getEyebrow())
        image = array(faceImage)
        return image

    def show(self, publish):
        image = self.buildFace()
        publish(image)

    # Reposition of the eyes of the baxter
    # This function provide with the eyes' simulation movement
    def lookWithMotion(self, cv2, destinationX, destinationY, time, publish):
        """
        Look with motion is a looking style with an animation
        Animation is generated like this:
            Eyes go to the given coordinates in a fiven time. in a loop
        """
        startTime = timeit.default_timer()
        currentTime = timeit.default_timer()
        x = self.eye.getPositionX()
        y = self.eye.getPositionY()

        while(self.eye.lookWithMotionCalculation(x, y, destinationX, destinationY, time, currentTime-startTime)):
            image = self.buildFace()
            publish(image) # this part is for the baxter's face
            currentTime = timeit.default_timer()

    """ 
    Dynamic looking functions are recalculates the x value according to the head of the Baxter's position
    if the goal coordinate is not in the angle of view of Baxter. -> Wobbling the head joint
    """

    def lookWithMotionDynamic(self, cv2, destinationX, destinationY, time, publish, wobbler):
        # if it is not initilized don't applicate the function
        if wobbler != None:
            # taking head position as a coordinate
            headPositionRadian = wobbler.getPosition()
            headPositionCoordinate = self.radianToCoordinate(headPositionRadian)
            # control for goal coordinate is not in the angle of view of Baxter
            if abs(destinationX - headPositionCoordinate) > self.radianToCoordinate(self.angleOfView):
                # wobbling -> look at the given coordinates physicly
                print "Wobbling to: ", destinationX
                wobbler.wobble(self.coordinateToRadian(destinationX))
                self.eye.lookExactCoordinate(0, destinationY)
                image = self.buildFace()
                publish(image)
            else:
                # Normal looking with eyes with an animation
                destinationX = destinationX - headPositionCoordinate
                self.lookWithMotion(cv2, destinationX, destinationY, time, publish)

    def lookExactCoordinateDynamic(self, destinationX, destinationY, publish, wobbler):
        # Looking the given coordinate according to the position of the head.
        if wobbler != None:
            # taking head position as a coordinate
            headPositionRadian = wobbler.getPosition()
            headPositionCoordinate = self.radianToCoordinate(headPositionRadian)
            # control for goal coordinate is not in the angle of view of Baxter
            if abs(destinationX - headPositionCoordinate) > self.radianToCoordinate(self.angleOfView):
                # wobbling -> look at the given coordinates physicly
                print "Wobbling to: ", destinationX
                wobbler.wobble(self.coordinateToRadian(destinationX))
                self.eye.lookExactCoordinate(0, destinationY)
            else:
                # Normal looking with eyes with an animation
                destinationX = destinationX - headPositionCoordinate
                self.eye.lookExactCoordinate(destinationX, destinationY)
            image = self.buildFace()
            publish(image)

    
    """
    Winkmove functions sets the position of the eyelid with an animation.
    """

    def winkMove(self, cv2, destinationPosition, time, publish):

        # Animation initial values
        startTime = timeit.default_timer()
        currentTime = timeit.default_timer()
        position = self.eyelid.getPosition()
        # Animation part
        while(self.eyelid.moveCalculation(position, destinationPosition, time, currentTime-startTime)):
            image = self.buildFace()
            publish(image)
            currentTime = timeit.default_timer()
            
    def wink(self, cv2, publish):
        firstPosition = self.eyelid.getPosition()
        self.winkMove(cv2, 0, 0.3, publish)
        self.winkMove(cv2, firstPosition, 0.2, publish)
        self.eyelid.setPosition(firstPosition)
        self.show(publish)

    # Encapsulation

    def getSkin(self):
        return self.skin

    def getMouth(self):
        return self.mouth

    def getEyebrow(self):
        return self.eyebrow

    def getEye(self):
        return self.eye

    def getEyelid(self):
        return self.eyelid

    def getBackgroundImage(self):
        return self.backgroundImage


    # Emotions

    def showEmotion(self, mouthIndex, eyebrowIndex, cv2, publish):
        #self.mouth.setMouth(mouthIndex)
        self.eyebrow.setEyebrow(eyebrowIndex)
        self.show(publish)

    def sleep(self, cv2, publish):
       self.winkMove(cv2, 0, 0.6, publish) # Eyelids are not seen.
       self.skin.setSkin(0) # range: [0, 5]
       self.showEmotion(1, 1, cv2, publish)

    def wakeUp(self, cv2, publish):
        self.winkMove(cv2, -330, 0.8, publish) # Eyelids are not seen.
        self.skin.setSkin(0) # range: [0, 5]
        self.showEmotion(5, 0, cv2, publish)

    def emotion_default(self, cv2, publish):
       self.winkMove(cv2, -330, 0.3, publish) # Eyelids are not seen.
       self.skin.setSkin(0)
       self.showEmotion(5, 0, cv2, publish)
    
    def emotion_happy(self, cv2, publish):
        mouthArray = [4, 6]
        eyeBrowArray = [0, 1]
        self.winkMove(cv2, -330, 0.3, publish) # Eyelids are not seen.
        self.skin.setSkin(0)
        mouthIndex = 4#random.choice(mouthArray)
        eyebrowIndex = 1#random.choice(eyeBrowArray)
        self.showEmotion(mouthIndex, eyebrowIndex, cv2, publish)

    def emotion_neutral(self, cv2, publish):
        eyeBrowArray = [0, 1]
        self.winkMove(cv2, -330, 0.3, publish)  # Eyelids are not seen.
        self.skin.setSkin(0)
        mouthIndex = 5  # random.choice(mouthArray)
        eyebrowIndex = 0#random.choice(eyeBrowArray)
        self.showEmotion(mouthIndex, eyebrowIndex, cv2, publish)

    def emotion_angry(self, cv2, publish):
        mouthArray = [0, 3]
        eyeBrowArray = [2, 3]
        self.winkMove(cv2, -330, 0.3, publish) # Eyelids are not seen.
        self.skin.setSkin(0)
        mouthIndex = random.choice(mouthArray)
        eyebrowIndex = 4#random.choice(eyeBrowArray)
        self.showEmotion(mouthIndex, eyebrowIndex, cv2, publish)

    def emotion_confused(self, cv2, publish):
        mouthArray = [2]
        eyeBrowArray = [0, 1]
        self.winkMove(cv2, -330, 0.3, publish) # Eyelids are not seen.
        self.skin.setSkin(0)
        mouthIndex = random.choice(mouthArray)
        eyebrowIndex = 3
        self.showEmotion(mouthIndex, eyebrowIndex, cv2, publish)

    def emotion_sad(self, cv2, publish):
        mouthArray = [1, 3]
        eyeBrowArray = [4]
        self.winkMove(cv2, -330, 0.3, publish) # Eyelids are not seen.
        self.skin.setSkin(0)
        mouthIndex = 1#random.choice(mouthArray)
        eyebrowIndex = 2#random.choice(eyeBrowArray)
        self.showEmotion(mouthIndex, eyebrowIndex, cv2, publish)

    def emotion_panic(self, cv2, publish):
        mouthArray = [2]
        eyeBrowArray = [1]
        self.winkMove(cv2, -330, 0.3, publish) # Eyelids are not seen.
        self.skin.setSkin(0)
        mouthIndex = random.choice(mouthArray)
        eyebrowIndex = random.choice(eyeBrowArray)
        self.showEmotion(mouthIndex, eyebrowIndex, cv2, publish)

    def emotion_bored(self, cv2, publish):
        mouthArray = [1]
        eyeBrowArray = [0, 2, 3]
        self.winkMove(cv2, -150, 0.3, publish) # Eyelids are in the middle of the eyes.
        self.skin.setSkin(0)
        mouthIndex = random.choice(mouthArray)
        eyebrowIndex = 2#random.choice(eyeBrowArray)
        self.showEmotion(mouthIndex, eyebrowIndex, cv2, publish)

    def emotion_crafty(self, cv2, publish):
        mouthArray = [4, 6]
        eyeBrowArray = [2, 3]
        self.winkMove(cv2, -330, 0.3, publish) # Eyelids are not seen.
        self.skin.setSkin(0)
        mouthIndex = 4#random.choice(mouthArray)
        eyebrowIndex = random.choice(eyeBrowArray)
        self.showEmotion(mouthIndex, eyebrowIndex, cv2, publish)



    """ Head Joint move calculations """

    def coordinateToRadian(self, theta) :
        return (3 * theta) / 160.0

    def radianToCoordinate(self, coordinate) :
        return (160 * coordinate) / 3

