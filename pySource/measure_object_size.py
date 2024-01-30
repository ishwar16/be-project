import cv2
from object_detector import *
import numpy as np
import os

path = 'E:/Ddrive/BE Project/pySource/Uploads'
#
# IMG_1 = "boxS"
# IMG_2 = "amz1"

arr = []
# Load Aruco detector
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

# Load Object Detector
detector = HomogeneousBgDetector()

def proccessIMG(imageName):
    # Load Image
    # img = cv2.imread("phone_aruco_marker.jpg")
    print(imageName)
    img = cv2.imread(os.path.join(path, imageName))


    # Get Aruco marker
    corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

    # Draw polygon around the marker
    int_corners = np.int0(corners)
    cv2.polylines(img, int_corners, True, (0, 0, 255), 10)

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

        print(round(object_height, 1), round(object_width, 1))

        # Display rectangle
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
        cv2.polylines(img, [box], True, (0, 255, 0), 5)
        cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
        cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

    arr.append(round(object_height, 1))
    arr.append(round(object_width, 1))

    # name = imageName + "_(" + str(round(object_height, 2)) + "x" + str(round(object_width, 2)) + ")" + ".jpeg"
    cv2.imwrite(os.path.join(path, imageName), img)
    print(arr)
    print("Succes!!")
    fr = "E:/Ddrive/BE Project/pySource/Uploads/" + imageName
    to = "E:/Ddrive/BE Project/pySource/static/Uploads/" + imageName
    os.replace(fr, to)
    return  str(arr)


def replace_with_avg(ar):
    # sort the array
    ar.sort()

    # initialize minimum difference to a large value
    min_diff = float('inf')

    # loop through the array and find the minimum difference
    for i in range(len(ar) - 1):
        diff = abs(ar[i] - ar[i + 1])
        if diff < min_diff:
            min_diff = diff

    # find the two values with minimum difference
    for i in range(len(ar) - 1):
        if abs(ar[i] - ar[i + 1]) == min_diff:
            val1 = ar[i]
            val2 = ar[i + 1]
            # delete the two values
            ar.remove(val1)
            ar.remove(val2)
            break

    # find the average of the two values
    avg = (val1 + val2) / 2

    # add the average to the array
    arr.append(avg)

    return ar

def volumeCalculation():
    arr.sort()
    print(arr)
    resultarr = replace_with_avg(arr)
    # x = round((arr[2] + arr[3])/2, 2)
    output = "Volume = " + str(resultarr[0]) + " x " + str(resultarr[1]) + " x " + str(resultarr[2]) + " cc = "
    print("Volume = " + str(resultarr[0]) + " x " + str(resultarr[1]) + " x " + str(resultarr[2]) + " cc")
    output = output + str(round(((resultarr[0])*(resultarr[1])*(resultarr[2])), 2))  + " cc"
    arr.clear()

    return output

# proccessIMG(IMG_1)
# proccessIMG(IMG_2)
# volumeCalculation()

# cv2.imshow("Image", img)
# print(object_height)
# print(object_width)
# cv2.waitKey(0)