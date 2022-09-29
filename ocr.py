import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytesseract


pytesseract.pytesseract.tesseract_cmd = R'C:\Program Files\Tesseract-OCR\tesseract'

img = cv2.imread('./image/img_crop_95.png')

text = pytesseract.image_to_string(img, config='--psm 13 --oem 1')
print(text)
