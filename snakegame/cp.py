from turtle import width
import cv2
from cv2 import VideoCapture 
from cvzone.HandTrackingModule import HandDetector
import cvzone
import math
import numpy as np
import random
import pygame
w,h=1280,720
pygame.init()
Snake_Window = pygame.display.set_mode([600,600])
pygame.display.set_caption("Snake_game")
pygame.display.update()
Clock = pygame.time.Clock()
cap=cv2.VideoCapture(0)
detector=HandDetector(detectionCon=0.8,maxHands=1)
while True:
    sucess,img=cap.read()
    img = cv2.resize(img,(600,600))
    hands, img = detector.findHands(img)
    if hands:
        hand1=hands[0]
        cx,cy=hand1['center']
        lmlist=hand1["lmList"]
        fingers=detector.fingersUp(hand1)
        print(lmlist[8][0],lmlist[8][1],fingers)
    cv2.imshow('Frame',img)
    key=cv2.waitKey(1)
    if key==ord('q'):
        break
    
