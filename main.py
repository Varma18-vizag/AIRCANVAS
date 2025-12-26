import cv2
import numpy as np
from collections import deque

def setvalues(x):
    print("")
    
cv2.namedWindow("color hsv")
cv2.createTrackbar("upper_hue","color hsv",170,180,setvalues)
cv2.createTrackbar("upper_saturation","color hsv",255,255,setvalues)    
cv2.createTrackbar("upper_value","color hsv",255,255,setvalues)
cv2.createTrackbar("lower_hue","color hsv",60,180,setvalues) 
cv2.createTrackbar("lower_saturation","color hsv",75,255,setvalues)    
cv2.createTrackbar("lower_value","color hsv",40,255,setvalues)    

bpoints =[deque(maxlen=1024)]  
rpoints =[deque(maxlen=1024)]
gpoints =[deque(maxlen=1024)]
ppoints =[deque(maxlen=1024)]

blue_index=0
red_index=0
green_index=0   
purple_index=0

kernel=np.ones((5,5),np.uint8)
colors = [(255,0,0),(0,0,255),(0,255,0),(255,105,180)]
colorIndex = 0
paintWindow=np.zeros((471,636,3)) + 255

paintWindow =cv2.rectangle(paintWindow,(30,1),(130,65),(0,0,0),2)
paintWindow =cv2.rectangle(paintWindow,(160,1),(255,65),colors[0],-1)
paintWindow =cv2.rectangle(paintWindow,(290,1),(385,65),colors[1],-1)
paintWindow =cv2.rectangle(paintWindow,(420,1),(515,65),colors[2],-1)
paintWindow =cv2.rectangle(paintWindow,(550,1),(635,65),colors[3],-1)
cv2.putText(paintWindow,"CLEAR",(49,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2,cv2.LINE_AA)
#cv2.namedWindow("Paint",cv2.WINDOW_AUTOSIZE)

cap=cv2.VideoCapture(0)
while True:
    success,frame=cap.read()
    frame=cv2.flip(frame,1)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    u_hue=cv2.getTrackbarPos("upper_hue","color hsv")
    u_saturation=cv2.getTrackbarPos("upper_saturation","color hsv")
    u_value=cv2.getTrackbarPos("upper_value","color hsv")
    l_hue=cv2.getTrackbarPos("lower_hue","color hsv")
    l_saturation=cv2.getTrackbarPos("lower_saturation","color hsv")
    l_value=cv2.getTrackbarPos("lower_value","color hsv")
    
    u_color=np.array([u_hue,u_saturation,u_value])
    l_color=np.array([l_hue,l_saturation,l_value])
    


    
    frame =cv2.rectangle(frame,(30,1),(130,65),(0,0,0),-1)
    frame =cv2.rectangle(frame,(160,1),(255,65),colors[0],-1)
    frame =cv2.rectangle(frame,(290,1),(385,65),colors[1],-1)
    frame =cv2.rectangle(frame,(420,1),(515,65),colors[2],-1)
    frame =cv2.rectangle(frame,(550,1),(635,65),colors[3],-1)
    cv2.putText(frame,"CLEAR",(49,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
    mask=cv2.inRange(hsv,l_color,u_color) 
    mask=cv2.erode(mask,kernel,iterations=1)
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel) 
    mask=cv2.dilate(mask,kernel,iterations=1)
    cnts,z=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center=None
    if len(cnts)>0:
        cnt=sorted(cnts,key=cv2.contourArea,reverse=True)[0]
        ((x,y),radius)=cv2.minEnclosingCircle(cnt)
        cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)
        M=cv2.moments(cnt)
        center=(int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        
        if center[1]<=65:
            if 30<=center[0]<=130:
                bpoints=[deque(maxlen=512)]  
                rpoints=[deque(maxlen=512)]
                gpoints=[deque(maxlen=512)]
                ppoints=[deque(maxlen=512)]

                blue_index=0
                red_index=0
                green_index=0   
                purple_index=0
                paintWindow[67:,:,:]=255
            elif 160<=center[0]<=255:
                colorIndex=0
            elif 290<=center[0]<=385:
                colorIndex=1
            elif 420<=center[0]<=515:
                colorIndex=2
            elif 550<=center[0]<=635:
                colorIndex=3
        else:
            if colorIndex==0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex==1:
                rpoints[red_index].appendleft(center)
            elif colorIndex==2:
                gpoints[green_index].appendleft(center)
            elif colorIndex==3:
                ppoints[purple_index].appendleft(center)
    else:
        bpoints.append(deque(maxlen=512))  
        blue_index+=1
        rpoints.append(deque(maxlen=512))
        red_index+=1
        gpoints.append(deque(maxlen=512))
        green_index+=1   
        ppoints.append(deque(maxlen=512))
        purple_index+=1
    
    points=[bpoints,rpoints,gpoints,ppoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1,len(points[i][j])):
                if points[i][j][k-1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame,points[i][j][k-1],points[i][j][k],colors[i],2)
                cv2.line(paintWindow,points[i][j][k-1],points[i][j][k],colors[i],2)
    cv2.imshow("White Window",paintWindow)
    cv2.imshow("Cam",frame)
    cv2.imshow("mask",mask)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()