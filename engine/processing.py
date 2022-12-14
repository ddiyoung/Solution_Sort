import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

class PngProcessing(object):
    def __init__(self):
        self.pngfile = ""
        self.img = object
        self.kernel = np.ones((3, 13), np.uint8)
        self.contour_pos = []
        self.min = 190
        self.max = 200
        self.h_range = [100, 200]
        self.w_range = [200, 300]
        self.contours = []


    def grayScale(self):
        self.img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        return self.img_gray

    def threshOld(self, min, max):
        _, self.thresh = cv2.threshold(self.img_gray, min, max, cv2.THRESH_BINARY_INV)
        return self.thresh

    def dilate(self):
        self.dilation = cv2.dilate(self.thresh, self.kernel, iterations=2)
        return self.dilation

    def close(self):
        self.closing = cv2.morphologyEx(self.dilation, cv2.MORPH_CLOSE, self.kernel)
        return self.closing

    def findContour(self):
        self.contours, self.hierarchy = cv2.findContours(self.closing, cv2.RETR_EXTERNAL, 3)
        return self.contours

    def boudingContour(self, h_range, w_range):
        for pos in range(len(self.contours)):
            x, y, w, h = cv2.boundingRect(self.contours[pos])

            if h_range[0] <= h <= h_range[1] and w_range[0] <= w <= w_range[1]:
                self.contour_pos.append(pos)
        
        return self.contour_pos
    
    def cropThresh(self):
        _, self.crop_thresh = cv2.threshold(self.img_gray, 227, 255, cv2.THRESH_BINARY_INV)
        return self.crop_thresh

    def cropImage(self):
        for pos in self.contour_pos:
            x, y , w, h = cv2.boundingRect(self.contours[pos])
            img_crop = self.crop_thresh[y:y + h, x: x+w]
            cv2.imwrite(f'./crop/{self.pngfile}/img_crop_{pos}.png', img_crop)

    def darwImage(self):
        img_copy = self.img.copy()

        img_contour = cv2.drawContours(img_copy, self.contours, -1, (0, 255, 0), 3)
        cv2.imwrite(f'./draw/{self.pngfile}/{self.pngfile}', img_contour)

    def run(self, Pngfile):
        self.pngfile = os.path.basename(Pngfile)
        os.makedirs(f'./crop/{self.pngfile}', exist_ok = True)
        os.makedirs(f'./draw/{self.pngfile}', exist_ok = True)

        self.img = cv2.imread(Pngfile)

        self.grayScale()
        self.threshOld(self.min, self.max)
        self.dilate()
        self.close()
        self.findContour()
        #self.darwImage()
        self.boudingContour(self.h_range, self.w_range)
        self.cropThresh()
        self.cropImage()