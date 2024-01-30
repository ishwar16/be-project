import cv2
from object_detector import *
import numpy as np
import os

IMG_1 = "boxS"
IMG_2 = "boxM"

arr = []
# Load Aruco detector
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

# Load Object Detector
detector = HomogeneousBgDetector()

def proccessIMG(imageName):
    # Load Image
    # img = cv2.imread("phone_aruco_marker.jpg")
    img = cv2.imread(imageName+".jpeg")


    # Get Aruco marker
    corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

    # Draw polygon around the marker
    int_corners = np.int0(corners)
    cv2.polylines(img, int_corners, True, (0, 0, 255), 5)

    # Aruco Perimeter
    aruco_perimeter = cv2.arcLength(corners[0], True)

    # Pixel to cm ratio
    pixel_cm_ratio = aruco_perimeter / 20

    contours = detector.detect_objects(img)

    # Draw objects boundaries
    for cnt in contours:
        # Get rect
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect

        # Get Width and Height of the Objects by applying the Ratio pixel to cm
        object_width = w / pixel_cm_ratio
        object_height = h / pixel_cm_ratio

        # Display rectangle
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
        cv2.polylines(img, [box], True, (255, 0, 0), 2)
        cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
        cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

        arr.append(round(object_height, 1))
        arr.append(round(object_width, 1))

        name = imageName + "_(" + str(round(object_height, 2)) + "x" + str(round(object_width, 2)) + ")" + ".jpeg"
        cv2.imwrite(name, img)
        print(arr)
        print("Succes!!")

def volumeCalculation():
    arr.sort()
    print(arr)
    x = round((arr[2] + arr[3])/2, 2)
    print("Volume = " + str(arr[0]) + " x " + str(arr[1]) + " x " + str(x) + " cc")
    print((arr[0])*(arr[1])*(x))

def lambda_handler(event=None, context=None):
    proccessIMG(IMG_1)
    proccessIMG(IMG_2)
    volumeCalculation()

# cv2.imshow("Image", img)
# print(object_height)
# print(object_width)
# cv2.waitKey(0)