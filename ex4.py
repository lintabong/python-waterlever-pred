import numpy
import cv2
import copy
import time

img   = cv2.imread('img/s2.jpeg')

print("image size:", img.shape)

maxHeight = 100

percentage = 60
width      = int(img.shape[1]*percentage/100)
height     = int(img.shape[0]*percentage/100)


  
img = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)

y = 100
x = 420
h = 800
w = 550

hsv   = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
mask1 = cv2.inRange(hsv, (0, 10, 120), (150, 240, 255))

img   = cv2.bitwise_and(img, img, mask=mask1)

croppedImg = img[y:h, x:w]
edges      = cv2.Canny(croppedImg, 0, 255)

rho             = 1
theta           = numpy.pi/180
threshold       = 15
min_line_length = 50
max_line_gap    = 20

lines = cv2.HoughLinesP(edges, rho, theta, threshold, numpy.array([]), min_line_length, max_line_gap)

if lines is not None:
    for line in lines:
        for x1, y1, x2, y2 in line:
            im = copy.deepcopy(croppedImg)
            cv2.line(im, (x1, y1), (x2, y2), (255, 0, 0), 1)

cv2.line(img, (x, y), (x+w-x, y), (255, 0, 255), 2)
cv2.line(img, (x, y+h-y), (x+w-x, y+h-y), (255, 0, 255), 2)
cv2.line(img, (x, y), (x, y+h-y), (255, 0, 255), 2)
cv2.line(img, (x+w-x, y), (x+w-x, y+h-y), (255, 0, 255), 2)
cv2.line(img, (x+int((w-x)/2), y), (x+int((w-x)/2), h), (255, 0, 255), 2)

for i in range(len(croppedImg)):
    for j in range(len(croppedImg[i])):
        if numpy.mean(croppedImg[i][j]) >= 136:
            croppedImg[i][j] = (0,0,0)

# for i in range(len(croppedImg)):
#     for j in range(len(croppedImg[i])):
#         print(croppedImg[i][j])

count = 0
for i in range(len(img)):
    for j in range(len(img[i])):
        if i == x+w-x and numpy.mean(img[i][j]) < 255 and numpy.mean(img[i][j]) > 0:
            count+=1

# font
font = cv2.FONT_HERSHEY_SIMPLEX
org = (580, 150)
fontScale = 1
color = (255, 0, 0)
thickness = 2

value = round(maxHeight-(count/(h-y))*30,2)
image = cv2.putText(img, str(value), org, font, fontScale, color, thickness, cv2.LINE_AA)



cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
