import cv2 
from cvzone.HandTrackingModule import HandDetector
import cvzone
import math
import numpy as np
import random
cap = cv2.VideoCapture(0)
cap.set(3,1200)
cap.set(4,1200)
detector = HandDetector(detectionCon=0.8, maxHands=1)
class SnakeGameclass:
    def __init__(self, pathFood):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous head point
 
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()
 
        self.score = 0
        self.gameOver = False
 
    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)
 
    def update(self, imgMain, currentHead):
 
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300, 400],
                               scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [300, 550],
                               scale=7, thickness=5, offset=20)
        else:
            px, py = self.previousHead
            cx, cy = currentHead
 
            self.points.append([cx, cy])
            distance = math.sqrt(pow(cx - px,2)+pow(cy - py,2))
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy
 
            # Length Reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break
 
            # Check if snake ate the Food
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                    ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
                print(self.score)
 
            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
                cv2.circle(imgMain, self.points[-1], 20, (0, 255, 0), cv2.FILLED)
 
            # Draw Food
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood,
                                        (rx - self.wFood // 2, ry - self.hFood // 2))
 
            cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80],
                               scale=3, thickness=3, offset=10)
 
            # Check for Collision
            pts = np.array(self.points[:-2], np.int32)
            print(pts)
            pts = pts.reshape((-1, 1, 2))
            print(pts)
            cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)
            print(minDist)
            if -0.5 <= minDist <= 0.5:
                print("Hit")
                self.gameOver = True
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed Length
                self.previousHead = 0, 0  # previous head point
                self.randomFoodLocation()
 
        return imgMain
    
game = SnakeGameclass('Donut.png')

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    # Find the hand and its landmarks
    hands, img = detector.findHands(img)
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]# List of 21 Landmark pointsq
        #point at 8-Indexfinger point
        pointIndex = lmList1[8][0:2] # print(pointIndex)
        img = game.update(img, pointIndex)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        game.gameOver = False
    if key== ord('q'):
        break
# Previous Lesson
cap.release()
cv2.destroyAllWindows()
 # img=np.zeros([512,512,3],np.uint8)
