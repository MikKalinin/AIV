import pyautogui
import time
import numpy as np
import cv2
import imutils

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

while True:
    pix = pyautogui.screenshot(region=(int(left), int(top), window_resolution[0], window_resolution[1]))
    numpix = cv2.cvtColor(np.array(pix), cv2.COLOR_RGB2BGR)
    numpix_hsv = cv2.cvtColor(np.array(pix), cv2.COLOR_RGB2HSV)

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

    result_g = cv2.bitwise_and(numpix, numpix, mask=mask_g)
    result_y = cv2.bitwise_and(numpix, numpix, mask=mask_y)
    result_r = cv2.bitwise_and(numpix, numpix, mask=mask_r)

    cv2.imshow('result_g', result_g)
    cv2.imshow('result_y', result_y)
    cv2.imshow('result_r', result_r)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
