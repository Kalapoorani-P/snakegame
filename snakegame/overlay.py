import queue
import stat
import cv2 
from cvzone.HandTrackingModule import HandDetector
import cvzone
import math
import numpy as np
import random
def randomFoodLocation():
    global img
    imgFood = cv2.imread('Donut.png', cv2.IMREAD_UNCHANGED)
    # cls.foodPoint = random.randint(100, 1000), random.randint(100, 600)
    hFood, wFood, _ = imgFood.shape
    Queue=[]
    if len(Queue)<10:
        rx,ry = random.randint(100, 1000), random.randint(100, 600)
        x = rx - wFood // 2
        y = ry - hFood // 2
        # imgMain = cvzone.overlayPNG(img, imgFood,(x, y))
        if [x,y] not in Queue:
            Queue.append([x,y])
    for i in Queue:
        cvzone.overlayPNG(img, imgFood,(x, y))
    return img
class Snakegame:
    def __init__(self):
        Snakegame.randomFoodLoctaion
cap = cv2.VideoCapture(0)
cap.set(3,1200)
cap.set(4,1200)
detector = HandDetector(detectionCon=0.8, maxHands=1)
count=0
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    if count==0:
        img=randomFoodLocation()
        count=1

    # Find the hand and its landmarks
    # hands, img = detector.findHands(img)
    # if hands:
    #     hand1 = hands[0]
    #     lmList1 = hand1["lmList"]# List of 21 Landmark pointsq
    #     #point at 8-Indexfinger point
    #     pointIndex = lmList1[8][0:2] # print(pointIndex)
  

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    # if key == ord('r'):
    #     game.gameOver = False
    if key== ord('q'):
        break
# Previous Lesson
cap.release()
cv2.destroyAllWindows()

