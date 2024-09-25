import cv2
import numpy as np

cor = np.uint8([[[56,145,232 ]]])
cor = cv2.cvtColor(cor,cv2.COLOR_BGR2HSV)
print(cor)