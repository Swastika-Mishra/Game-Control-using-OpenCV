import mediapipe as mp
import cv2
import numpy as np
import pyautogui
import time
import threading

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

mpHands = mp.solutions.hands
hands=mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
mpDraw=mp.solutions.drawing_utils

def right():
    print("right")
    pyautogui.keyDown("right")
    pyautogui.keyUp("right")
    time.sleep(2)
def left():
    print("left")
    pyautogui.keyDown("left")
    pyautogui.keyUp("left")
    time.sleep(2)
def up():
    print("up")
    pyautogui.keyDown("up")
    pyautogui.keyUp("up")
    time.sleep(2)
def down():
    print("down")
    pyautogui.keyDown("down")
    pyautogui.keyUp("down")
    time.sleep(2)

thread1=threading.Thread(target=right)
thread2=threading.Thread(target=left)
thread3=threading.Thread(target=up)
thread4=threading.Thread(target=down)

while cap.isOpened():
    success, img = cap.read()
    img=cv2.flip(img,2)
    imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            if(handLms.landmark[16].y<handLms.landmark[14].y and handLms.landmark[7].y<handLms.landmark[6].y):
                if not thread3.is_alive():
                    try:
                        thread3.start()
                    except RuntimeError:
                        thread3=threading.Thread(target=up)
                        thread3.start()
            elif(handLms.landmark[8].y<handLms.landmark[5].y and handLms.landmark[12].y<handLms.landmark[9].y):
                if not thread4.is_alive():
                    try:
                        thread4.start()
                    except RuntimeError:
                        thread4=threading.Thread(target=down)
                        thread4.start()
            elif(handLms.landmark[7].y<handLms.landmark[6].y):
                a=np.array([[handLms.landmark[8].x], [handLms.landmark[8].y]])
                b=np.array([[handLms.landmark[5].x], [handLms.landmark[5].y]])
                c=np.array([[handLms.landmark[0].x], [handLms.landmark[0].y]])
                rad=np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
                ang=np.abs(rad*180/np.pi)
                if(ang>=180):
                    if not thread2.is_alive():
                        try:
                            thread2.start()
                        except RuntimeError:
                            thread2=threading.Thread(target=left)
                            thread2.start()
                elif(ang<180):
                    if not thread1.is_alive():
                        try:
                            thread1.start()
                        except RuntimeError:
                            thread1=threading.Thread(target=right)
                            thread1.start()
            else:
                continue
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()