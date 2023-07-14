import cv2
import numpy
import matplotlib.pyplot as plt
from matplotlib import colors

img = cv2.imread("img/p4.png", cv2.IMREAD_COLOR)

hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

mask = cv2.inRange(hsv_img, (0, 0, 200), (145, 60, 255))

result = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("image", result)

cv2.waitKey(0)
cv2.destroyAllWindows()