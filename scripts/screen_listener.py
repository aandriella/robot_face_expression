#!/usr/bin/env python

'''
@Author: Bilgehan NAL
This file is a subscriber node which listens a topic type:String
Waited String messages:
Emotions:
    -> "default"
    -> "happy"
    -> "sad"
    -> "angry"
    -> "confused"
    -> "panic"
    -> "bored"
Actions:
    -> "look_<x>_<y>"
    -> "look_<x>_<y>_<time>"
    -> "wake_up"
    -> "sleep"
Other:
    -> "exit"
    -> "wake_up"
    -> "sleep"


'''

import os
import sys
import rospy
import timeit
import cv2
import cv_bridge
import Face
from sensor_msgs.msg import Image, PointCloud
from std_msgs.msg import String
import threading
#import head_wobbler
#from baxter_core_msgs.msg import EndpointState
import math

""" Variable Decleration """

wobbler = None

face = Face.Face()
defaultMsg = "This message is for controlling the msgs (is it the same with previous one?)"


# helpers: handle the noise while following the human

isSystemRun = True

def isInAvailablePercentage(minimum, current, percentage):
    rangeOfPercentage = percentage / 100.0
    if abs(current-minimum) < (minimum * rangeOfPercentage):
        return True
    else:
        return False

# publish image is a function which displays the image given with parameter. Image Type: Numpy array
def publish_image(img):
    msg = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="rgba8")
    pub = rospy.Publisher('/robot/expression_diplay', Image, latch=True, queue_size=1)
    pub.publish(msg)

# Statistical Functions
def mode(numbers) :
    largestCount = 0
    modes = []
    for x in numbers:
        if x in modes:
            continue
        count = numbers.count(x)
        if count > largestCount:
            del modes[:]
            modes.append(x)
            largestCount = count
        elif count == largestCount:
            modes.append(x)
    return modes[0]

def stddev(lst):
    mean = float(sum(lst)) / len(lst)
    return (float(reduce(lambda x, y: x + y, map(lambda x: (x - mean) ** 2, lst))) / len(lst))**0.5

def mean(listX) :
    return sum(listX) / len(listX)

def eliminateOutliers(listOfData, limit) :
    stdDeviation = stddev(listOfData)
    meanOfList = mean(listOfData)

    for element in listOfData :
        if stdDeviation != 0 :
            zScore = abs(element - meanOfList) / stdDeviation
            if zScore > limit :
                del element
    return listOfData

""" Callback Functions """

def callback_Command(data):
    global isSystemRun
    global defaultMsg
    global humanFollowControl
    global armFollowControl
    global isItLeftArm
    global dynamicControl
    msg = data.data.lower() # All lethers were made in small to compare.
    print "recieved msg is : {}".format(msg)
    msgs = msg.split("_") #this array keeps all variables
   
    # Messages and actions

    if len(msgs) == 1 and msg != defaultMsg:
        
        if msgs[0] == "default" :
            face.emotion_default(cv2, publish_image)
            print "Default Emotion is applicated"

        if msgs[0] == "happy" :
            face.emotion_happy(cv2, publish_image)
            print "Emotion happy is applicated"

        elif msgs[0] == "angry" :
            face.emotion_angry(cv2, publish_image)
            print "Emotion angry is applicated"

        elif msgs[0] == "confused" :
            face.emotion_confused(cv2, publish_image)
            print "Emotion confused is applicated"

        elif msgs[0] == "sad" :
            face.emotion_sad(cv2, publish_image)
            print "Emotion sad is applicated"

        elif msgs[0] == "panic" :
            face.emotion_panic(cv2, publish_image)
            print "Emotion panic is applicated"

        elif msgs[0] == "bored" :
            face.emotion_bored(cv2, publish_image)
            print "Emotion bored is applicated"

        elif msgs[0] == "crafty" :
            face.emotion_crafty(cv2, publish_image)
            print "Emotion crafty is applicated"

        elif msgs[0] == "neutral":
            face.emotion_default(cv2, publish_image)
            print "Emotion neutral is applicated"

        elif msgs[0] == "wakeup":
            face.wakeUp(cv2, publish_image)
            print "Emotion wakeup is applied"

        elif msgs[0] == "exit" :
            print "Program is closing..."
            face.sleep(cv2, publish_image)
            rospy.sleep(1)
            print "Program is closed"
            isSystemRun = False
            sys.exit()

        elif msgs[0] == "sleep" :
            face.sleep(cv2, publish_image)
            print "Sst! Baxter is sleeping right now"
            
        defaultMsg = msg
    
    elif len(msgs) == 2 and msg != defaultMsg :

        if msgs[0] == "skin" :
            numberOfSkin = int(msgs[1]) 
            face.skin.setSkin(numberOfSkin)
            face.show(publish_image)
        
        elif msgs[0] == "wake" and msgs[1] == "up" :
            face.wakeUp(cv2, publish_image)
            print "Baxter woke up"

        defaultMsg = msg

    elif len(msgs) == 3 and msg != defaultMsg :
        if msgs[0] == "look" :
            x = int(msgs[1])
            y = int(msgs[2])
            face.lookWithMotion(cv2, x, y, 0.8, publish_image)


    
    elif len(msgs) == 4 and msg != defaultMsg :
        if msgs[0] == "look" :
            x = int(msgs[1])
            y = int(msgs[2])
            second = float(msgs[3])
            face.lookWithMotion(cv2, x, y, second, publish_image)



def main():
    global wobbler
    print "entered main part..."
#    wobbler = head_wobbler.Wobbler()
    #face.testAllImages(cv2, publish_image)
    face.emotion_neutral(cv2, publish_image)
    #face.sleep(cv2, publish_image)
#    rospy.Subscriber('/robot/sonar/head_sonar/state', PointCloud, callback_human_follow)
#    rospy.Subscriber('/robot/limb/left/endpoint_state', EndpointState, callback_left_arm_follow)
#    rospy.Subscriber('/robot/limb/right/endpoint_state', EndpointState, callback_right_arm_follow)
    rospy.Subscriber('facial_expression', String, callback_Command)
    rospy.spin()
    return 0

def main_loop() :
    global isSystemRun
    rospy.sleep(2)
    rate = rospy.Rate(10) #10 times in a second (loop frequency)
    #These time keepers for the eyelid
    referenceTime = timeit.default_timer()
    currentTime = timeit.default_timer()
    print "entered main loop part..."

    while not rospy.is_shutdown() :
        
        # Blink for each 5 seconds.
        currentTime = timeit.default_timer()
        if currentTime - referenceTime > 5:
            face.wink(cv2, publish_image)
            referenceTime = timeit.default_timer()
            print "wink motion is applicated"

        if isSystemRun == False :
            sys.exit()
    
    face.show(publish_image)
    isSystemRun = False

if __name__ == '__main__' :

    rospy.init_node('rsdk_xdisplay_image', anonymous=True)
    
    threadMain = threading.Thread(name='listener', target=main)
    threadMainLoop = threading.Thread(name='main_loop', target=main_loop)

    try:
        threadMain.daemon = True
        threadMainLoop.daemon = True
        threadMainLoop.start()
        threadMain.start()
    except (KeyboardInterrupt, SystemExit):
        cleanup_stop_thread()
        sys.exit()

    except :
        print "Unable to start thread"
    while 1 :
        if isSystemRun == False :
            break
        pass
