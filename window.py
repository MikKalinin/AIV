import pyautogui
import time
import numpy as np
import cv2
import imutils
from main import q, th

print('waiting for 2 seconds...')
time.sleep(2)

title = './logo1.png'

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
'''
th.start()

ranges = {
    'min_h1': {'current': 70, 'max': 180},
    'max_h1': {'current': 82, 'max': 180},
    'min_s1': {'current': 82, 'max': 255},
    'max_s1': {'current': 82, 'max': 255},
    'min_v1': {'current': 82, 'max': 255},
    'max_v1': {'current': 82, 'max': 255},
}


def trackbar_handler(name):
    def handler(x):
        global ranges
        ranges[name]['current'] = x

    return handler


for name in ranges:
    cv2.createTrackbar(name,
                       'result',
                       ranges[name]['current'],
                       ranges[name]['max'],
                       trackbar_handler(name)
                       )
'''

while True:
    pix = pyautogui.screenshot(region=(int(left), int(top), window_resolution[0], window_resolution[1]))
    numpix = cv2.cvtColor(np.array(pix), cv2.COLOR_RGB2BGR)
    numpix = cv2.GaussianBlur(numpix, (5, 5), 0)
#    numpix = numpix[window_resolution[1]//2:, :, :]
    numpix_hsv = cv2.cvtColor(np.array(pix), cv2.COLOR_RGB2HSV)
#    numpix_hsv = numpix_hsv[window_resolution[1]//2:, :, :]

    min_g = (45, 50, 90)
    max_g = (68, 255, 255)

    min_y = (28, 100, 100)
    max_y = (32, 255, 255)

    min_r1 = (0, 130, 40)
    max_r1 = (21, 160, 170)
    min_r2 = (155, 135, 40)
    max_r2 = (180, 155, 180)

    mask_g = cv2.inRange(numpix_hsv, min_g, max_g)
    mask_y = cv2.inRange(numpix_hsv, min_y, max_y)
    mask_r1 = cv2.inRange(numpix_hsv, min_r1, max_r1)
    mask_r2 = cv2.inRange(numpix_hsv, min_r2, max_r2)
    mask_r = cv2.bitwise_or(mask_r1, mask_r2)

    mask = cv2.bitwise_or(mask_g, mask_y)
    mask = cv2.bitwise_or(mask, mask_r)

    result = cv2.bitwise_and(numpix, numpix, mask=mask_g)

    X = result.shape[0]
    Y = result.shape[1]
    startP = (Y//2, X)

    contours = cv2.findContours(mask_g, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = contours[0]
    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        cv2.drawContours(result, contours, -1, (255, 0, 0), 1)
        idx = 0
        (x, y, w, h) = cv2.boundingRect(contours[idx])

        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 1)

        (x1, y1), radius = cv2.minEnclosingCircle(contours[idx])
        center = (int(x1), int(y1))
        radius = int(radius)

        cv2.circle(result, center, radius, (0, 255, 0), 1)
        cv2.line(result, startP, center, (0, 255, 0), 1)

        track = x1 - Y//2

        if q.empty():
            q.put(track)
#    cv2.imshow('mask', mask_g)
    cv2.imshow('result', result)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
q.put(None)
th.join()
