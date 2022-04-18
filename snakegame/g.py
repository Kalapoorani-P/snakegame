from pickle import TRUE
from re import S
import pygame
import random
import cv2
import mediapipe as mp 
import cvzone 
from cvzone.HandTrackingModule import HandDetector
import math
class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,25)*SIZE
        self.y = random.randint(1,20)*SIZE
class SnakeGameclass:
    def __init__(self):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous head point
        self.block=pygame.image.load('block.jpg').convert()
        self.imgFood = cv2.imread('Donut.png', cv2.IMREAD_UNCHANGED)
        self.Food=pygame.image.load('Donut.png').convert()
        # self.x=120
        # self.y=120 
        # self.hFood, self.wFood, _ = self.imgFood.shape
        self.hFood=self.Food.get_height()
        self.wFood= self.Food.get_width()
        # self.foodPoint = 0, 0
        self.randomFoodLocation()
        
        self.score = 0
    def randomFoodLocation(self):
            self.foodPoint = random.randint(100, 1000), random.randint(100, 600)
    def update(self,imgMain,currentHead):
        px, py = self.previousHead
        cx, cy = currentHead
        self.points.append([cx, cy])
        distance = math.hypot(cx - px, cy - py)
        self.lengths.append(distance)
        self.currentLength += distance
        self.previousHead = cx, cy
        # Draw Snake
        # Length Reduction
        if self.currentLength > self.allowedLength:
            for i, length in enumerate(self.lengths):
                # imgMain.fill((5,5,5))
                self.currentLength -= length
                self.lengths.pop(i)
                self.points.pop(i)
                if self.currentLength < self.allowedLength:
                    break
        # Check if snake ate the Food
        rx, ry = self.foodPoint
        if rx - self.wFood// 2 < cx < rx + self.wFood // 2 and \
                ry - self.hFood // 2 < cy < ry + self.hFood // 2:
            self.randomFoodLocation()
            self.allowedLength += 50
            self.score += 1
            print(self.score)
         # Draw Food
        imgMain.blit(self.Food,((rx - self.wFood // 2, ry - self.hFood // 2)))
        pygame.display.update()
 
        if self.points:
            for i, point in enumerate(self.points):
                if i != 0:
                    # imgMain.blit(self.block,self.points[i-1][0]-self.points[i][0],self.points[i-1][-1]-self.points[i][-1])
                    # imgMain.fill((5,5,5))
                    # pygame.time.wait(100)
                    imgMain.blit(self.block,(self.points[i-1][0],self.points[i-1][-1]))
                    imgMain.blit(self.block,(self.points[i][0],self.points[i][-1]))
                    # self.points[i-1][0]-=40
                    # self.points[i-1][-1]-=40
                    # pygame.display.flip()


                    # pygame.draw.rect(imgMain,(133,67,67),pygame.Rect(self.points[][],self.points[0])

                    # print(self.points[-1][)
                    pygame.display.update()
        
cap = cv2.VideoCapture(0)
cap.set(3,600)
cap.set(4,600)
detector = HandDetector(detectionCon=0.8, maxHands=1)
pygame.init()
Snake_Window = pygame.display.set_mode([600,600])
pygame.display.set_caption("Snake_game")
Snake_Window.fill((5,5,5))
pygame.display.update()
running=True
game= SnakeGameclass()
while running:
    succes,img=cap.read()
    img = cv2.flip(img,1)
    hands, img = detector.findHands(img)
    # for event in pygame.event.get():
        # img = cv2.flip(img,1)
        # hands, img = detector.findHands(img)
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]# List of 21 Landmark pointsq
        #point at 8-Indexfinger point
        pointIndex = lmList1[8][0:2]
        # for event in pygame.event.get():
        for event in pygame.event.get():
            if event==pygame.QUIT:
                running=False
        game.update(Snake_Window,pointIndex)
        cv2.imshow("Image", img)
        for event in pygame.event.get():
            if event==pygame.QUIT:
                running=False

    if cv2.waitKey(1) & 0xFF==ord('q'):
        running=False
        # if event.type==pygame.QUIT:
        #     running=False
cap.release()
cv2.destroyAllWindows()
