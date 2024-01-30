import cv2
from object_detector import *
import numpy as np
from flask import Flask,render_template,Response


# Load Aruco detector
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)


# Load Object Detector
detector = HomogeneousBgDetector()

# Load Cap
cap = cv2.VideoCapture(0)
address = "https://192.168.188.144:8080/video"
cap.open(address)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

app = Flask(__name__)
# camera = cv2.VideoCapture(0)

# while True:
#     _, img = cap.read()
#
#     # Get Aruco marker
#     corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
#     if corners:
#
#         # Draw polygon around the marker
#         int_corners = np.int0(corners)
#         cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
#
#         # Aruco Perimeter
#         aruco_perimeter = cv2.arcLength(corners[0], True)
#
#         # Pixel to cm ratio
#         pixel_cm_ratio = aruco_perimeter / 20
#
#         contours = detector.detect_objects(img)
#
#         # Draw objects boundaries
#         for cnt in contours:
#             # Get rect
#             rect = cv2.minAreaRect(cnt)
#             (x, y), (w, h), angle = rect
#
#             # Get Width and Height of the Objects by applying the Ratio pixel to cm
#             object_width = w / pixel_cm_ratio
#             object_height = h / pixel_cm_ratio
#
#             # Display rectangle
#             box = cv2.boxPoints(rect)
#             box = np.int0(box)
#
#             cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
#             cv2.polylines(img, [box], True, (255, 0, 0), 2)
#             cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
#             cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
#
#
#
#     cv2.imshow("Image", img)
#     key = cv2.waitKey(1)
#     if key == 27:
#         break

def generate_frames():
    while True:

        ## read the camera frame
        success, frame = cap.read()
        if not success:
            break
        else:
            rec, img = cap.read()

            # Get Aruco marker
            corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
            if corners:
                # Draw polygon around the marker
                int_corners = np.int0(corners)
                cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

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

                    print(object_height, object_width)

                    # Display rectangle
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)

                    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
                    cv2.polylines(img, [box], True, (255, 0, 0), 2)
                    cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)),
                                cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
                    cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)),
                                cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

            rec, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('videoStream.html')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(debug=True, host="localhost", port=8080)

cap.release()
cv2.destroyAllWindows()