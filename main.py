from HandTrackingModule import handDetector
import cv2
import math
from time import sleep
import numpy as np
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = handDetector()

#Создаём кнопки клавиатуры
buttonlist=[]
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
         ["A","S","D","F","G","H","J","K","L",";"],
         ["Z","X","C","V","B","N","M",".","!","?"]]
text=""
for i in range(len(keys)):
        for j,key in enumerate(keys[i]):
            buttonlist.append(Button(img,[100*j+50,100*i+50],key))
        
class Button():
    def __init__(self,img,position,text,size=[85,85]):
        self.position = position
        self.size = size
        self.text = text

def drawButtons(img,buttonlist):
    for button in buttonlist:
        x,y=button.position
        w,h =button.size
        cv2.rectangle(img,button.position,(x+w,y+h),(0,0,250),cv2.FILLED)
        cv2.putText(img,button.text,(button.position[0]+15,button.position[1]+65),cv2.FONT_HERSHEY_COMPLEX_SMALL,4,(255,255,255),4)
    return img         

# def drawtranspButtons(img,buttonlist):
#     newimg=np.zeros_like(img,np.uint8)
#     for button in buttonlist:
#         x,y=button.position
#         w,h =button.size
#         cvzone.cornerRect(img,button.position[0],button.position[1],button.size[0],button.size[1],20,rt=0)
        
#         cv2.rectangle(img,button.position,(x+w,y+h),(0,0,250),cv2.FILLED)
#         cv2.putText(img,button.text,(button.position[0]+15,button.position[1]+65),cv2.FONT_HERSHEY_COMPLEX_SMALL,4,(255,255,255),4)
        
#     out = img.copy()
#     alpha = 0.5
#     mask = newimg.astype(bool)
#     out[mask]= cv2.addWeighted(img,alpha,newimg,1-alpha,0)[mask]
#     return img  
    


def isclicked(): #если расстояние между кончиками большого и указательного пальца маленькое, то считаем что нажали на клавишу
    x1,y1 = lmlist[8][1],lmlist[8][2]
    x2,y2 = lmlist[4][1],lmlist[4][2]
    distance = math.hypot(x2-x1,y2-y1)
    if distance < 30:
        return True
    
    
        
while True:
    success,img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img,draw = False)
    img = drawButtons(img,buttonlist)
    
    if lmlist: #если на кадре найдена ладонь
        
        for button in buttonlist:
            x,y = button.position
            w,h = button.size
            
            if x < lmlist[8][1] < x+w and y<lmlist[8][2]<y+h: #указательный палец находится на кнопке
                  cv2.rectangle(img,button.position,(x+w,y+h),(0,0,150),cv2.FILLED)
                  cv2.putText(img,button.text,(x+15,y+65),cv2.FONT_HERSHEY_COMPLEX_SMALL,4,(255,255,255),4)
                  
                  if isclicked():
                      cv2.rectangle(img,button.position,(x+w,y+h),(0,250,0),cv2.FILLED)
                      cv2.putText(img,button.text,(x+15,y+65),cv2.FONT_HERSHEY_COMPLEX_SMALL,4,(255,255,255),4)
                      text+=button.text
                      sleep(0.2)
    cv2.rectangle(img,(50,350),(700,450),(0,250,0),cv2.FILLED)
    cv2.putText(img,text,(60,425),cv2.FONT_HERSHEY_COMPLEX_SMALL,4,(255,255,255),4)
                                       
    
    cv2.imshow("IMAGE",img)
    cv2.waitKey(1)

