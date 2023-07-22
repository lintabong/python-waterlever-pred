import cv2
import numpy

cap = cv2.VideoCapture("vid/p1.mp4")
  
y = 100
x = 420
h = 800
w = 550



if (cap.isOpened()== False):
    print("Error opening video file")
  
while(cap.isOpened()):      
    ret, img = cap.read()

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

    cv2.imshow('Frame', img)
          
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
  
cap.release()
cv2.destroyAllWindows()