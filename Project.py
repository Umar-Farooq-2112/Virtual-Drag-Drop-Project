import cv2 
from cvzone.HandTrackingModule import HandDetector

w_cam,h_cam = 1200,800

capture = cv2.VideoCapture(0)

capture.set(3,w_cam)
capture.set(4,h_cam)

detector = HandDetector(detectionCon=int(0.8))


class Rectangle():
    def __init__(self,centerPos,size =(200,200)):
        self.centerPos = centerPos
        self.size =size
        self.color = (255,255,255)
    def update(self,position):
        cx,cy = self.centerPos
        w,h = self.size
        
        if cx-w//2<position[0]<cx+w//2 and cy-h//2<position[1]<cy+h//2:
                self.centerPos= position
                self.color = (0,0,0)
        else:
            self.color = (255,255,255)
rectangles = []
for i in range(2):
    rectangles.append(Rectangle([i*250+100,200]))

while True:
    status, img = capture.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmlist,_ = detector.findPosition(img)
    if lmlist:
        l,_,_ = detector.findDistance(8,12,img)
        
        if l<30:
            for rectangle in rectangles:
                rectangle.update(lmlist[8])

    for rectangle in rectangles:
        cx,cy = rectangle.centerPos
        w,h = rectangle.size
        cv2.rectangle(img,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),rectangle.color,thickness=8)
    cv2.imshow('Capture',img)
    if cv2.waitKey(20) & 0xFF==ord('d'):
        break