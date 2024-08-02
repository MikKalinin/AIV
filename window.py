import pyautogui
import time
import numpy as np
import cv2
import imutils
from main import q, th, pid
import keyboard

print('waiting for 2 seconds...')
time.sleep(2)

title = './logo1.png'

contlist = list()
contorsize = list()
timer1 = 0
t1 = 0
tf = 0
megamoveFlag = 0
megamoveFlag2 = 0
firstFlag1 = 0
pidt = 0
pidt2 = 0
kayw = 'start'

nfs_window_location = None
searching_attempt = 1
while searching_attempt <= 5:
    nfs_window_location = pyautogui.locateOnScreen(title)

    if nfs_window_location is not None:
        break
    else:
        searching_attempt += 1
        time.sleep(1)

if nfs_window_location is None:
    print('NFS Window not found')
    exit(1)

left = nfs_window_location[0]
top = nfs_window_location[1]+nfs_window_location[3]

window_resolution = (800, 600)

cv2.namedWindow('result')

th.start()

while True:
    pix = pyautogui.screenshot(region=(int(left), int(top), window_resolution[0], window_resolution[1]))
    numpix = cv2.cvtColor(np.array(pix), cv2.COLOR_RGB2BGR)
    numpix = cv2.GaussianBlur(numpix, (5, 5), 0)
    numpix = numpix[window_resolution[1]//2:, :, :]
    numpix_hsv = cv2.cvtColor(np.array(pix), cv2.COLOR_RGB2HSV)
    numpix_hsv = numpix_hsv[window_resolution[1]//2:, :, :]

    min_g = (50, 120, 90)
    max_g = (69, 220, 220)

    min_y = (30, 100, 100)
    max_y = (32, 255, 255)

    min_r1 = (0, 130, 40)
    max_r1 = (21, 160, 170)
    min_r2 = (155, 135, 40)
    max_r2 = (180, 155, 180)

    mask_g = cv2.inRange(numpix_hsv, min_g, max_g)
    mask_y = cv2.inRange(numpix_hsv, min_y, max_y)
    mask_r1 = cv2.inRange(numpix_hsv, min_r1, max_r1)
    mask_r2 = cv2.inRange(numpix_hsv, min_r2, max_r2)

    mask = cv2.bitwise_or(mask_g, mask_y)
    mask = cv2.bitwise_or(mask, mask_r1)
    mask = cv2.bitwise_or(mask, mask_r2)

    mask_r = cv2.bitwise_or(mask_r1, mask_r2)

    result = cv2.bitwise_and(numpix, numpix)

    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = contours[0]

    X = result.shape[0]
    Y = result.shape[1]
    startP = (Y//2, X)

    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        cv2.drawContours(result, contours, -1, (255, 0, 0), 1)

        for id in range(len(contours)):
            (x, y, w, h) = cv2.boundingRect(contours[id])

            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 1)

            contlist.append((x + w // 2, y + h // 2))

            (x1, y1), radius = cv2.minEnclosingCircle(contours[id])
            center = (int(x1), int(y1))
            radius = int(radius)


            cv2.circle(result, center, radius, (0, 255, 0), 1)
            cv2.line(result, startP, center, (0, 255, 0), 1)

            track = x1 - Y//2

            if q.empty():
                q.put(track)

    max_large = 0
    pass_x = 0
    poss_y = 0
    poss_x1 = 0
    poss_y1 = 0
    max_id = len(contours)-1

    for id in range(len(contours)):
        poss_x1, poss_y1 = contlist[id]
        if max_id == id:
            poss_x, poss_y = contlist[id]

    if t1 + 0.1 < time.perf_counter():
        t1 = time.perf_counter()
        tf = 1
    else:
        tf = 0
    tf = 1

    xm, ym = pyautogui.position()
    xw, yw, _, _ = nfs_window_location

    pidt = time.perf_counter() - pidt2
    if xm > xw and xm < xw + window_resolution[0] and ym > yw and ym < yw + window_resolution[1] and megamoveFlag == 0:
        if poss_x != 0:
            pidg = pid(poss_x, startP[0], 10.0, -0.2, 0.2, pidt, -1, 1)
            if pidg == -1:
                time.sleep(0.01)
                kayw = 'd'
                image = cv2.putText(numpix, 'd' + str(poss_x), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                time.sleep(0.2)
                pidt2 = time.perf_counter()
            elif pidg == 1:
                time.sleep(0.01)
                kayw = 'a'
                image = cv2.putText(numpix, 'a' + str(poss_x), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                time.sleep(0.2)
                pidt2 = time.perf_counter()

        if len(contlist) == 0 and megamoveFlag == 0:
            image = cv2.putText(numpix, 'f', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            if kayw == 'd':
                image = cv2.putText(numpix, 'fd', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                time.sleep(0.05)
            elif kayw == 'a':
                image = cv2.putText(numpix, 'fa', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                time.sleep(0.05)
    if megamoveFlag == 1:
        image = cv2.putText(numpix, 'w', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    contlist = []
    contorsize = []

    cv2.imshow('result', result)
    cv2.imshow('mask', mask)

    if megamoveFlag == 0:
        time.sleep(0.01)

    if keyboard.is_pressed('t'):
        if megamoveFlag == 0 and megamoveFlag2 == 1:
            megamoveFlag = 1
            megamoveFlag2 = 0
        elif megamoveFlag == 1 and megamoveFlag2 == 1:
            megamoveFlag = 0
            megamoveFlag2 = 0
            time.sleep(5)
    else:
        megamoveFlag2 = 1
    if firstFlag1 == 0:
        time.sleep(3)
        firstFlag1 = 1

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
