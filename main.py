import cv2 
import time
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0,(640, 480))

#Starting the webcam
cap = cv2.VideoCapture(0)

#Allowing the webcam to warmup by making the code stop for 2 seconds(thereby using sleep function)
time.sleep(2)

#Background
bg=0

for i in range(60):
    ret, bg = cap.read()

#Flipping the background
bg = np.flip(bg, axis=1)

while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    #Flipping the image for consistency
    img = np.flip(img , axis = 1)
    #Converting the colour from bgr(blue,green,red) to hsv(hue,saturation,value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #Generating mask to detect red color
    #Note: these values can also be changed as per the color
    lower_red=np.array([0,120,50])
    upper_red=np,array([10,255,255])
    mask_1 = cv2.inRange(hsv,lower_red, upper_red)
    #Creating another mask to detect red color
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask_2 = cv2.inRange(hsv, lower_red, upper_red)
    #Combining the two masks
    mask_1 = mask_1 + mask_2
    mask_1 = cv2.morphologyEx(mask_1, pv2.MORPH_OPEN, np.ones(3,3), np.uint8)
    mask_1 = cv2.morphologyEx(mask_1, pv2.MORPH_DILATE, np.ones(3,3), np.uint8)
    #Collecting only the path that does not have mask_1 and saving in mask_2
    mask_2 = cv2.bitwise_not(mask_1)
    #Keeping only the part of the images without the red colour
    res_1 = cv2.bitwise_and(img, img, mask = mask_2)
    res_2 = cv2.bitwise_and(bg, bg, mask = mask_1)
    #Generating the final output by merging res_1, res_2
    final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)
    output_file.write(final_output)
    #Displaying the output to the user
    cv2.imshow()