import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

class PngProcessing(object):
    def __init__(self):
        self.pngfile = ""
        self.img = object
        self.kernel = np.ones((6, 15), np.uint8)
        self.contour_pos = []
        self.min = 180
        self.max = 190
        self.h_range = 6
        self.w_range = 15
        self.contours = []


    def grayScale(self):
        self.img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        return self.img_gray

    def threshOld(self, min, max):
        #if not self.img_gray:
         #   self.grayScale()
        
        _, self.thresh = cv2.threshhold(self.img_gray, min, max, cv2.THRESH_BINARY_INV)
        return self.thresh

    def dilate(self):
        if not self.thresh:
            self.threshOld(self.min, self.max)
        
        self.dilation = cv2.dilate(self.thresh, self.kernel, iteration=2)
        return self.dilation

    def close(self):
        if not self.dilation :
            self.dilate()
        
        self.closing = cv2.morphologyEx(self.dilate, cv2.MORPH_CLOSE, self.kernel)
        return self.closing

    def findContour(self):
        print(self.closing)

        if not self.closing:
            self.close()

        self.contours, self.hierarchy = cv2.findContours(self.closing, cv2.RETR_EXTERNAL, 3)
        return self.contours

    def boudingContour(self, h_range, w_range):
        if not self.contours:
            self.findContour()

        for pos in range(len(self.contours)):
            x, y, w, h = cv2.boundingRect(self.contours[pos])

            if h_range[0] <= h <= h_range[1] and w_range[0] <= w <= h_range[1]:
                self.contour_pos.append(pos)
        
        return self.contour_pos
    
    def cropThresh(self):
        if not self.img_gray:
            self.grayScale()
        
        _, self.crop_thresh = cv2.threshold(self.img_gray, 227, 255, cv2.THRESH_BINARY_INV)
        return self.crop_thresh

    def cropImage(self):
        if not self.contour_pos :
            self.boudingContour(self.h_range, self.w_range)

        if not self.crop_thresh:
                self.cropThresh()

        for pos in range(len(self.contours)):
            x, y , w, h = cv2.boundingRect(self.contours[pos])
            img_crop = self.crop_thresh[y:y + h, x: x+w]
            cv2.imwrite(f'./crop/{self.pngfile}/img_crop_{pos}.png', img_crop)

    def run(self, Pngfile):
        self.pngfile = os.path.basename(Pngfile)
        os.makedirs(f'./crop/{self.pngfile}', exist_ok = True)

        self.img = cv2.imread(Pngfile)

        self.grayScale()
        self.threshOld(self.min, self.max)
        self.dilate()
        self.close()
        self.findContour()
        self.boudingContour(self.h_range, self.w_range)
        self.cropThresh()
        self.cropImage()
        return 0