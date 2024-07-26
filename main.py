#работа с изображением (блюр, зеркалка, чб)

import cv2
import os

img2 = cv2.imread('./data/road-signs/approaching-a-pedestrian-crossing.jpg', cv2.IMREAD_GRAYSCALE)
img = cv2.imread('./data/road-signs/approaching-a-pedestrian-crossing.jpg')
img3 = cv2.imread('./data/road-signs/approaching-a-pedestrian-crossing.jpg')
img4 = cv2.imread('./data/road-signs/approaching-a-pedestrian-crossing.jpg')

if img is None:
    print("фото не найдено.")
    os._exit(1)
'''
x_max = img.shape[0]
y_max = img.shape[1]

x1, y1 = map(int, input().split(' '))
x2, y2 = map(int, input().split(' '))

cv2.imshow('img1', img[x1:x2+1, y1:y2+1])
'''

max_x = img.shape[0]
max_y = img.shape[1]

for x in range(0, max_x):
    for y in range(2, max_y//2):
        img3[x, max_y-y+1] = img3[x, y]

ksize = list(map(int, input().split(' ')))
img4 = cv2.blur(img4, ksize)

cv2.imshow('img', img)
cv2.imshow('img2', img2)
cv2.imshow('img3', img3)
cv2.imshow('img4', img4)
while True:
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
