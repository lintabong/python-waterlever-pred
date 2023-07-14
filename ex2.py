import numpy as np
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = "c:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

BGR = cv2.imread("img/p1.png")
RGB = cv2.cvtColor(BGR, cv2.COLOR_BGR2RGB)

hsv_img = cv2.cvtColor(RGB, cv2.COLOR_RGB2HSV)

mask  = cv2.inRange(hsv_img, (0, 0, 200), (145, 60, 255))
img   = cv2.bitwise_and(RGB, RGB, mask=mask)

img   = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV)[1]

gauss = cv2.GaussianBlur(img, (3,3), 1)
gauss[gauss<220] = 0

cv2.imshow("image", gauss)

text = pytesseract.image_to_string(gauss, config="outputbase digits")
text = pytesseract.image_to_string(gauss, config="--psm 7")
# --psm 7

print(text)

cv2.waitKey(0)
cv2.destroyAllWindows()