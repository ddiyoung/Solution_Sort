import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

img = cv2.imread('./image/image.png')
#img = cv2.resize(img, (600, 1200))

img_temp = img.copy()

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# cv2.imshow('img_gray', img_gray)

#plt.hist(img_gray.ravel(), 256, [0, 256])
#plt.show()

_, thresh = cv2.threshold(img_gray, 190, 200, cv2.THRESH_BINARY_INV)


kernel = np.ones((3, 9), np.uint8)

dilation = cv2.dilate(thresh, kernel, iterations=2)

closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)

cv2.imwrite('./image/closing.png', closing)

contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, 3)

img_contour = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
cv2.imwrite('./image/img_contour.png', img_contour)


contour_pos = []

for pos in range(len(contours)):
    x, y, w, h = cv2.boundingRect(contours[pos])
    if 35 < h < 50 and 60 < w < 80:
        contour_pos.append(pos)


_, thresh = cv2.threshold(img_gray, 227, 255, cv2.THRESH_BINARY_INV)

for pos in contour_pos:
    x, y, w, h = cv2.boundingRect(contours[pos])
    img_crop = thresh[y:y + h, x:x + w]
    cv2.imwrite(f'./image/img_crop_{pos}.png', img_crop)


#cv2.imshow('dilation', img)
# cv2.waitKey()
