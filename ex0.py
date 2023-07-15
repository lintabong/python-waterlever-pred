# import os
# import cv2
# import pytesseract

# pytesseract.pytesseract.tesseract_cmd = 'c:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

# img = cv2.imread("img/p2.png")
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
 
# dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

# contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
#                                                  cv2.CHAIN_APPROX_NONE)
 
# # Creating a copy of image
# im2 = img.copy()
 
# # A text file is created and flushed
# file = open("recognized.txt", "w+")
# file.write("")
# file.close()

# for cnt in contours:
#     x, y, w, h = cv2.boundingRect(cnt)

#     rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

#     cropped = im2[y:y + h, x:x + w]

#     file = open("recognized.txt", "a")

#     text = pytesseract.image_to_string(cropped)

#     file.write(text)
#     file.write("\n")

#     file.close
import numpy
print(numpy.mean([148, 136, 126]))