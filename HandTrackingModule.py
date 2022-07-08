import cv2
import mediapipe as mp
import time



previousTime =0
currentTime = 0
mpHands = mp.solutions.hands
hands = mpHands.Hands() #Создаём модель руки
mpDraw = mp.solutions.drawing_utils #рисовать ключевые точки на ладони 



   

class handDetector(): #создаём свой класс для детектора, чтобы было более удобно взаимодействовать с получаемыми данными
    def __init__(self,mode=False,maxHands =2,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands() #Создаём модель руки
        self.mpDraw = mp.solutions.drawing_utils #рисовать ключевые точки на ладони 

    def findHands(self,img,draw=True):
        img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks: #если на кадре замечена ладонь
            for each_hand in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, each_hand,self.mpHands.HAND_CONNECTIONS)
            
        return img

    def findPosition(self,img,handnum=0,draw=True):
        landmarklist =[]
        if self.results.multi_hand_landmarks: #если на кадре замечена ладонь
            myhand=self.results.multi_hand_landmarks[handnum]
            for id,landmark in enumerate(myhand.landmark):
                height,width,_ = img.shape
                cx,cy = int(landmark.x*width),int(landmark.y*height)
                landmarklist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),25,(250,150,122),cv2.FILLED)
                #print(id,cx,cy) #выводит все ключевые точки и их координаты, что позволяет обращаться к каждой ключевой точке по отдельности
        return landmarklist
        
        
        
        
        
        
        
def main():
    cap = cv2.VideoCapture(0)
    previousTime =0
    currentTime = 0
    detector = handDetector()
    while True:
        success,img = cap.read()
        
        img = detector.findHands(img,draw=False)
        lmlist = detector.findPosition(img)
        if len(lmlist) !=0:
            print(lmlist[4])
        
        currentTime = time.time()
        fps = 1/(currentTime-previousTime)
        previousTime=currentTime
        
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_ITALIC,3,(0.0,240.2,12.5),2)
        cv2.imshow("IMAGE",img)
        cv2.waitKey(1)
            
    

if __name__ == '__main__':
    main()    
    