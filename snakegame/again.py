import cv2
from cv2 import CAP_PROP_FRAME_WIDTH
from cv2 import CAP_PROP_FRAME_HEIGHT 
from cvzone.HandTrackingModule import HandDetector
import cvzone
import math
import numpy as np
import random

class Game:

    imgFood = cv2.imread('Donut.png', cv2.IMREAD_UNCHANGED) # Food image 
    hFood, wFood, _ = imgFood.shape # Height and width of Food image
    foodPoint = 0, 0 # Staring Food position

    def __init__(self):
        self.gameover=False 
        self.randomFoodLocation() 
        self.player1=Player()
        self.player2=Player()
    
    # Generate Random Food position 
    def randomFoodLocation(cls):
        Game.foodPoint = random.randint(200, 800), random.randint(200, 600)

    def update(self,imgMain):
        # If game over display score and the winner
        if self.gameover:
            cvzone.putTextRect(imgMain, "Game Over", [300, 300],
                            scale = 7, thickness = 5, offset = 20)
            if self.player1.score>self.player2.score:
                cvzone.putTextRect(imgMain, f'Player 1 wins!!: {self.player1.score}', [100, 550],
                                scale = 5, thickness = 3, offset = 10)
            else:
                cvzone.putTextRect(imgMain, f'Player 2 wins!!: {self.player2.score}', [100, 550],
                                scale=5, thickness = 3, offset=10)
               
        else:
            # Random Food position 
            rx,ry = Game.foodPoint

            # # Find the hand and its landmarks
            hands, imgMain = detector.findHands(imgMain)

            if hands:
                # Hand 1
                hand1 = hands[0]
                lmList1 = hand1["lmList"]  # List of 21 Landmark points
                pointIndex = lmList1[8][0:2] # Index Finger 

                cv2.rectangle(imgMain, (0,0),(1400,1400), (5,5,5), cv2.FILLED)
              
                imgMain = cvzone.overlayPNG(imgMain, Game.imgFood,(rx - Game.wFood // 2, ry - Game.hFood // 2)) # Overlay Food
               
                if hand1['type']=='Left':
                    imgMain = self.player1.update(imgMain,pointIndex,(23,45,78),rx,ry,Game.wFood,Game.hFood,1)  # Hand type left consider as player 1
                else:
                    imgMain = self.player2.update(imgMain,pointIndex,(123,45,78),rx,ry,Game.wFood,Game.hFood,2) # Hand type right consider as player 2
                
                if len(hands)==2:
                    hand2 = hands[1]
                    lmList2 = hand2["lmList"]
                    pointIndex= lmList2[8][0:2]
                    if hand2['type'] == "Left":
                        imgMain = self.player1.update(imgMain,pointIndex,(23,45,78),rx,ry,Game.wFood,Game.hFood,1)
                    else:
                        imgMain = self.player2.update(imgMain, pointIndex,(123,45,67),rx,ry,Game.wFood,Game.hFood,2)
                
        return imgMain

class Player(Game):
    def __init__(self):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous head point
        self.score = 0
    def update(self,imgMain,currHead,color,rx,ry,wFood,hFood,player):
        # Previous position of index finger
        px, py = self.previousHead

        # Current position of index finger
        cx, cy = currHead


        self.points.append([cx, cy])
        distance = math.sqrt(pow(cx - px,2)+pow(cy - py,2))  # Calculating distance between two points 
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

        # Snake ate the food
        if rx -wFood // 2 < cx < rx + wFood // 2 and \
                ry - hFood // 2 < cy < ry + hFood // 2:
            self.randomFoodLocation()
            self.score += 1
            print(self.score)
        print(rx,wFood,ry,hFood)

        # Draw snake body 
        if self.points:
            for i, point in enumerate(self.points):
                if i != 0:
                    cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
            cv2.circle(imgMain, self.points[-1], 20, color, cv2.FILLED)
        
        # Score of Player 1
        if player==1:
            cvzone.putTextRect(imgMain, f'Player 1 Score: {self.score}', [50, 80],
                               scale=3, thickness=3, offset=10)

        # Score of player 2
        if player==2:
            cvzone.putTextRect(imgMain, f'Player 2 Score: {self.score}', [50, 150],
                               scale=3, thickness=3, offset=10)

        return imgMain


if __name__ == "__main__":

    # Video Capture
    cap = cv2.VideoCapture(0)

    # Setting capture window width
    cap.set(CAP_PROP_FRAME_WIDTH,1200)

    # Setting capture window width
    cap.set(CAP_PROP_FRAME_HEIGHT,1200)

    # Hand Detector
    detector = HandDetector(detectionCon=0.8, maxHands=2)

    # Game object
    game=Game()

    #Game Status
    StartGame=False

    # Timer variable 
    timer=100*10

    while True:
        # Capture image frame-by-frame  
        success, img = cap.read()

        # Starting Frame
        if not StartGame :
            cvzone.putTextRect(img,f'Opencv-Snake Game',[200,200], scale=3, thickness=3)
            cvzone.putTextRect(img,f"Press 'S' to Begin",[200,350])
        else:
            # Flipping image
            img = cv2.flip(img,1)

            # Game Frame Updates
            img = game.update(img)

            # If game not over display timer on the top right corner
            if game.gameover == False:
                x = timer//100
                cvzone.putTextRect(img,f'Time Left {x} secs',[800,150], scale=3, thickness=3)
            timer -= 1
            # If timer becomes zero set GameOver as True 
            if timer <= 0:
                game.gameover=True

        # Display captured Frame
        cv2.imshow("Image", img)

        # Wait untill the a key is pressed
        key = cv2.waitKey(1)

        # key to start the game 
        if key == ord('s'):
            StartGame=True
        
        # Key to restart the game 
        if key == ord('r'):
            game.gameover = False
            t = 100*11
            game.player1.score = 0
            game.player2.score = 0
        
        # key to Quit the game 
        if key == ord('q'):
            break

       
    # Release the captured video
    cap.release()
    cv2.destroyAllWindows()